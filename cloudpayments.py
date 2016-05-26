import json
import requests
from requests.auth import HTTPBasicAuth


class Currency(object):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'


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
                    email=None, data=None):
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

        response = self._send_request('payments/cards/charge', params)

        if response['Success']:
            return response['Model']
        if response['Message']:
            raise CloudPaymentsError(response)
        if 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise Secure3dAuthenticationRequiredException(response)

    def finish_3d_secure(self, transaction_id, pa_res):
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = self._send_request('payments/cards/post3ds', params)

        if response['Success']:
            return response['Model']

        raise CloudPaymentsError(response)

    def charge_token(self, account_id, token, amount, currency,
                     ip_address=None, invoice_id=None, description=None,
                     email=None, data=None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'AccountId': account_id,
            'Token': token,
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

        response = self._send_request('payments/tokens/charge', params)

        if response['Success']:
            return response['Model']
        if 'Model' in response and 'ReasonCode' in response['Model']:
            raise PaymentError(response)
        raise CloudPaymentsError(response)