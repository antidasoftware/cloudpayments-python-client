class ReasonCode(object):
    APPROVED = 0
    REFER_TO_CARD_ISSUER = 5001
    DO_NOT_HONOR = 5005
    ERROR = 5006
    INVALID_TRANSACTION = 5012
    AMOUNT_ERROR = 5013
    FORMAT_ERROR = 5030
    BANK_NOT_SUPPORTED_BY_SWITCH = 5031
    SUSPECTED_FRAUD = 5034
    LOST_CARD = 5041
    STOLEN_CARD = 5043
    INSUFFICIENT_FUNDS = 5051
    EXPIRED_CARD = 5054
    TRANSACTION_NOT_PERMITTED = 5057
    EXCEED_WITHDRAWAL_FREQUENCY = 5065
    INCORRECT_CVV = 5082
    TIMEOUT = 5091
    CANNOT_REACH_NETWORK = 5092
    SYSTEM_ERROR = 5096
    UNABLE_TO_PROCESS = 5204
    AUTHENTICATION_FAILED = 5206
    AUTHENTICATION_UNAVAILABLE = 5207
    ANTI_FRAUD = 5300


class TransactionStatus(object):
    AWAITING_AUTHENTICATION = 'AwaitingAuthentication'
    AUTHORIZED = 'Authorized'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    DECLINED = 'Declined'


class SubscriptionStatus(object):
    ACTIVE = 'Active'
    PAST_DUE = 'PastDue'
    CANCELLED = 'Cancelled'
    REJECTED = 'Rejected'
    EXPIRED = 'Expired'


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
