import json
import requests
from requests.auth import HTTPBasicAuth


class Currency(object):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'


class CloudPaymentsError(Exception):
    pass


class CloudPayments(object):
    URL = 'https://api.cloudpayments.ru/'

    def __init__(self, public_id, api_secret):
        self.public_id = public_id
        self.api_secret = api_secret

    def _send_request(self, endpoint, params=None):
        auth = HTTPBasicAuth(self.public_id, self.api_secret)
        response = requests.post(self.URL + endpoint,
                                 data=params, auth=auth).json()
        if not response['Success']:
            raise CloudPaymentsError(response['Message'])
        return response.get('Model')

    def test(self):
        return self._send_request('test')

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
        return self._send_request('payments/cards/charge', params)

    def finish_3d_secure(self, transaction_id, pa_res):
        params = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        return self._send_request('payments/cards/post3ds', params)

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
        return self._send_request('payments/tokens/charge', params)