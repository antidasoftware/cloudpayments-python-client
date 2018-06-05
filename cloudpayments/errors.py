from .enums import ERROR_MESSAGES


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
        self.transaction_id = response['Model']['TransactionId']
        super(PaymentError, self).__init__(response, self.reason)

    @property
    def verbose_reason(self):
        if self.reason_code not in ERROR_MESSAGES:
            return None
        return ERROR_MESSAGES[self.reason_code][0]

    @property
    def verbose_message(self):
        if self.reason_code not in ERROR_MESSAGES:
            return None
        return ERROR_MESSAGES[self.reason_code][1]
