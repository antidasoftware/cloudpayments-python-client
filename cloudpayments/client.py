import decimal

import requests
from requests.auth import HTTPBasicAuth

from .errors import CloudPaymentsError, PaymentError
from .models import Transaction, Secure3d, Subscription, Order, Receipt
from .utils import format_datetime, format_date


class CloudPayments(object):
    URL = 'https://api.cloudpayments.ru/'

    def __init__(self, public_id, api_secret):
        self.public_id = public_id
        self.api_secret = api_secret

    def _send_request(self, endpoint, params=None, request_id=None):
        auth = HTTPBasicAuth(self.public_id, self.api_secret)

        headers = None
        if request_id is not None:
            headers = {'X-Request-ID': request_id}

        response = requests.post(self.URL + endpoint, json=params, auth=auth, 
                                 headers=headers)
        return response.json(parse_float=decimal.Decimal)

    def test(self, request_id=None):
        response = self._send_request('test', request_id=request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)
        return response['Message']

    def get_transaction(self, transaction_id):
        """Get transaction info by its id."""
        params = {'TransactionId': transaction_id}
        response = self._send_request('payments/get', params)
        if 'Model' in response.keys():
            return Transaction.from_dict(response['Model'])
        else:
            raise CloudPaymentsError(response)

    def charge_card(self, cryptogram, amount, currency, name, ip_address,
                    invoice_id=None, description=None, account_id=None,
                    email=None, data=None, require_confirmation=False,
                    service_fee=None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'IpAddress': ip_address,
            'Name': name,
            'CardCryptogramPacket': cryptogram
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if description is not None:
            params['Description'] = description
        if account_id is not None:
            params['AccountId'] = account_id
        if email is not None:
            params['Email'] = email
        if service_fee is not None:
            params['PayerServiceFee'] = service_fee
        if data is not None:
            params['JsonData'] = data

        endpoint = ('payments/cards/auth' if require_confirmation else
                    'payments/cards/charge')
        response = self._send_request(endpoint, params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if response['Message']:
            raise CloudPaymentsError(response)
        if 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        return Secure3d.from_dict(response['Model'])

    def finish_3d_secure_authentication(self, transaction_id, pa_res):
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = self._send_request('payments/cards/post3ds', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise PaymentError(response)

    def charge_token(self, token, account_id, amount, currency,
                     ip_address=None, invoice_id=None, description=None,
                     email=None, data=None, require_confirmation=False):
        params = {
            'Amount': amount,
            'Currency': currency,
            'AccountId': account_id,
            'Token': token
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if description is not None:
            params['Description'] = description
        if ip_address is not None:
            params['IpAddress'] = ip_address
        if email is not None:
            params['Email'] = email
        if data is not None:
            params['JsonData'] = data

        endpoint = ('payments/tokens/auth' if require_confirmation else
                    'payments/tokens/charge')
        response = self._send_request(endpoint, params)
        if response['Success']:
            return Transaction.from_dict(response['Model'])
        if 'Model' in response and 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise CloudPaymentsError(response)

    def confirm_payment(self, transaction_id, amount, data=None):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }

        if data is not None:
            params['JsonData'] = data

        response = self._send_request('payments/confirm', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def void_payment(self, transaction_id):
        params = {'TransactionId': transaction_id}
        response = self._send_request('payments/void', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def refund(self, transaction_id, amount, request_id=None):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }
        response = self._send_request('payments/refund', params, request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)

        return response['Model']['TransactionId']

    def topup(self, token, amount, account_id, currency, invoice_id=None):
        params = {
            'Token': token,
            'Amount': amount,
            'AccountId': account_id,
            'Currency': currency
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        response = self._send_request('payments/cards/topup', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])

        raise CloudPaymentsError(response)

    def find_payment(self, invoice_id):
        params = {'InvoiceId': invoice_id}
        response = self._send_request('payments/find', params)

        if response['Success']:
            return Transaction.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    def list_payments(self, date, timezone=None):
        params = {'Date': format_date(date)}
        if timezone is not None:
            params['Timezone'] = timezone

        response = self._send_request('payments/list', params)

        if response['Success']:
            return map(Transaction.from_dict, response['Model'])
        raise CloudPaymentsError(response)

    def create_subscription(self, token, account_id, amount, currency,
                            description, email, start_date, interval, period,
                            require_confirmation=False, max_periods=None):
        params = {
            'Token': token,
            'AccountId': account_id,
            'Description': description,
            'Email': email,
            'Amount': amount,
            'Currency': currency,
            'RequireConfiramtion': require_confirmation,
            'StartDate': format_datetime(start_date),
            'Interval': interval,
            'Period': period,
        }
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = self._send_request('subscriptions/create', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    def list_subscriptions(self, account_id):
        params = {'accountId': account_id}
        response = self._send_request('subscriptions/find', params)

        if response['Success']:
            return map(Subscription.from_dict, response['Model'])
        raise CloudPaymentsError(response)

        
    def get_subscription(self, subscription_id):
        params = {'Id': subscription_id}
        response = self._send_request('subscriptions/get', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    def update_subscription(self, subscription_id, amount=None, currency=None,
                            description=None, start_date=None, interval=None,
                            period=None, require_confirmation=None,
                            max_periods=None):
        params = {
            'Id': subscription_id
        }
        if description is not None:
            params['Description'] = description
        if amount is not None:
            params['Amount'] = amount
        if currency is not None:
            params['Currency'] = currency
        if require_confirmation is not None:
            params['RequireConfirmation'] = require_confirmation
        if start_date is not None:
            params['StartDate'] = format_datetime(start_date)
        if interval is not None:
            params['Interval'] = interval
        if period is not None:
            params['Period'] = period
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = self._send_request('subscriptions/update', params)

        if response['Success']:
            return Subscription.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    def cancel_subscription(self, subscription_id):
        params = {'Id': subscription_id}

        response = self._send_request('subscriptions/cancel', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def create_order(self, amount, currency, description, email=None,
                     send_email=None, require_confirmation=None,
                     invoice_id=None, account_id=None, phone=None,
                     send_sms=None, send_whatsapp=None, culture_info=None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'Description': description,
        }
        if email is not None:
            params['Email'] = email
        if require_confirmation is not None:
            params['RequireConfirmation'] = require_confirmation
        if send_email is not None:
            params['SendEmail'] = send_email
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if account_id is not None:
            params['AccountId'] = account_id
        if phone is not None:
            params['Phone'] = phone
        if send_sms is not None:
            params['SendSms'] = send_sms
        if send_whatsapp is not None:
            params['SendWhatsApp'] = send_whatsapp
        if culture_info is not None:
            params['CultureInfo'] = culture_info

        response = self._send_request('orders/create', params)

        if response['Success']:
            return Order.from_dict(response['Model'])
        raise CloudPaymentsError(response)

    def create_receipt(self, inn, receipt_type, customer_receipt, 
                       invoice_id=None, account_id=None, request_id=None):
        if isinstance(customer_receipt, Receipt):
            customer_receipt = customer_receipt.to_dict()

        params = {
            'Inn': inn,
            'Type': receipt_type,
            'CustomerReceipt': customer_receipt,
        }
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if account_id is not None:
            params['AccountId'] = account_id

        response = self._send_request('kkt/receipt', params, request_id)

        if not response['Success']:
            raise CloudPaymentsError(response)
        return response['Model']['Id']

    def get_receipt(self, receipt_id):
        params = {'Id': receipt_id}
        response = self._send_request('kkt/receipt/get', params)

        if response['Success']:
            return Receipt.from_dict(response['Model'])
        raise CloudPaymentsError(response)
