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
        super(PaymentError, self).__init__(response, self.reason)
