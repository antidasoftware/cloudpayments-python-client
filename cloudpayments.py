import requests
from requests.auth import HTTPBasicAuth


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

