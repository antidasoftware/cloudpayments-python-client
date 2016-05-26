import json
import requests
from requests.auth import HTTPBasicAuth


class Currency(object):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'


class Interval(object):
    WEEK = 'Week'
    MONTH = 'Month'


class Timezone(object):
    HST = 'HST'
    AKST = 'AKST'
    PST = 'PST'
    MST = 'MST'
    CST = 'CST'
    EST = 'EST'
    AST = 'AST'
    BRT = 'BRT'
    UTC = 'UTC'
    GMT = 'GMT'
    CET = 'CET'
    EET = 'EET'
    MSK = 'MSK'
    AZT = 'AZT'
    AMT = 'AMT'
    SAMT = 'SAMT'
    GET = 'GET'
    TJT = 'TJT'
    YEKT = 'YEKT'
    ALMT = 'ALMT'
    NOVT = 'NOVT'
    KRAT = 'KRAT'
    HKT = 'HKT'
    IRKT = 'IRKT'
    SGT = 'SGT'
    ULAT = 'ULAT'
    YAKT = 'YAKT'
    VLAT = 'VLAT'
    SAKT = 'SAKT'
    ANAT = 'ANAT'


class CultureInfo(object):
    RU_RU = 'ru-RU'
    EN_US = 'en-US'


class CloudPaymentsError(Exception):
    def __init__(self, response, message=None):
        self.response = response
        super(CloudPaymentsError, self).__init__(message or
                                                 response.get('Message'))


class Secure3dAuthenticationRequiredException(CloudPaymentsError):
    def __init__(self, response):
        self.transaction_id = response['Model']['TransactionId']
        self.pa_req = response['Model']['PaReq']
        super(Secure3dAuthenticationRequiredException, self).__init__(response)


class PaymentError(CloudPaymentsError):
    def __init__(self, response):
        self.reason = response['Model']['Reason']
        self.reason_code = response['Model']['ReasonCode']
        super(PaymentError, self).__init__(response)


class CloudPayments(object):
    URL = 'https://api.cloudpayments.ru/'

    def __init__(self, public_id, api_secret):
        self.public_id = public_id
        self.api_secret = api_secret

    def _send_request(self, endpoint, params=None):
        auth = HTTPBasicAuth(self.public_id, self.api_secret)
        response = requests.post(self.URL + endpoint, data=params, auth=auth)
        return response.json()

    def test(self):
        response = self._send_request('test')
        if not response['Success']:
            raise CloudPaymentsError(response)

    def charge_card(self, cryptogram, amount, currency, name, ip_address,
                    invoice_id=None, description=None, account_id=None,
                    email=None, data=None, with_auth=False):
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
        if data is not None:
            params['JsonData'] = json.dumps(data)

        endpoint = ('payments/cards/auth' if with_auth else
                    'payments/cards/charge')
        response = self._send_request(endpoint, params)

        if response['Success']:
            return response['Model']
        if response['Message']:
            raise CloudPaymentsError(response)
        if 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise Secure3dAuthenticationRequiredException(response)

    def finish_3d_secure_authentication(self, transaction_id, pa_res):
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = self._send_request('payments/cards/post3ds', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    def charge_token(self, token, account_id, amount, currency,
                     ip_address=None, invoice_id=None, description=None,
                     email=None, data=None, with_auth=False):
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
            params['JsonData'] = json.dumps(data)

        endpoint = ('payments/tokens/auth' if with_auth else
                    'payments/tokens/charge')
        response = self._send_request(endpoint, params)

        if response['Success']:
            return response['Model']
        if 'Model' in response and 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise CloudPaymentsError(response)

    def confirm_payment(self, transaction_id, amount):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }
        response = self._send_request('payments/confirm', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def void_payment(self, transaction_id):
        params = {'TransactionId': transaction_id}
        response = self._send_request('payments/void', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def refund(self, transaction_id, amount):
        params = {
            'Amount': amount,
            'TransactionId': transaction_id
        }
        response = self._send_request('payments/refund', params)

        if not response['Success']:
            raise CloudPaymentsError(response)

    def find_payment(self, invoice_id):
        params = {'InvoiceId': invoice_id}
        response = self._send_request('payments/find', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    def list_payments(self, date, timezone=None):
        params = {'Date': date.isoformat()}
        if timezone is not None:
            params['Timezone'] = timezone

        response = self._send_request('payments/list', params)

        if response['Success']:
            return response['Model']
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
            'StartDate': start_date.isoformat(),
            'Interval': interval,
            'Period': period,
        }
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = self._send_request('subscriptions/create', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    def get_subscription(self, subscription_id):
        params = {'Id': subscription_id}
        response = self._send_request('subscriptions/get', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    def update_subscription(self, subscription_id, amount=None, currency=None,
                            description=None, start_date=None, interval=None,
                            period=None, require_confirmation=None,
                            max_periods=None):
        params  = {
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
            params['StartDate'] = start_date.isoformat()
        if interval is not None:
            params['Interval'] = interval
        if period is not None:
            params['Period'] = period
        if max_periods is not None:
            params['MaxPeriods'] = max_periods

        response = self._send_request('subscriptions/update', params)

        if response['Success']:
            return response['Model']
        raise CloudPaymentsError(response)

    def cancel_subscription(self, subscription_id):
        params = {'SubscriptionId': subscription_id}

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
            return response['Model']
        raise CloudPaymentsError(response)


