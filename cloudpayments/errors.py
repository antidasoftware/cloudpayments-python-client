class CloudPaymentsError(Exception):
    def __init__(self, response, message=None):
        self.response = response
        super(CloudPaymentsError, self).__init__(message or
                                                 response.get('Message'))


class PaymentError(CloudPaymentsError):
    def __init__(self, response):
        self.reason = response['Model']['Reason']
        self.reason_code = response['Model']['ReasonCode']
        self.cardholder_message = response['Model']['CardHolderMessage']
        super(PaymentError, self).__init__(response, self.reason)
