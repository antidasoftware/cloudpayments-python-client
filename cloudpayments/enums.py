# coding=utf-8
from __future__ import unicode_literals


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


ERROR_MESSAGES = {
    5001: ('Отказ эмитента проводить онлайн операцию', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5005: ('Отказ эмитента без объяснения причин', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5006: ('Отказ сети проводить операцию или неправильный CVV код', 
           'Проверьте правильность введенных данных карты или воспользуйтесь ' + 
           'другой картой'),
    5007: ('Карта потеряна',
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5012: ('Карта не предназначена для онлайн платежей', 
           'Воспользуйтесь другой картой или свяжитесь с банком, выпустившим ' + 
           'карту'),
    5013: ('Слишком маленькая или слишком большая сумма операции', 
           'Проверьте корректность суммы'),
    5014: ('Некорректный номер карты',
           'Проверьте правильность введенных данных карты или ' +
           'воспользуйтесь другой картой'),
    5030: ('Ошибка на стороне эквайера — неверно сформирована транзакция', 
           'Повторите попытку позже'),
    5031: ('Неизвестный эмитент карты', 'Воспользуйтесь другой картой'),
    5034: ('Отказ эмитента — подозрение на мошенничество', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5041: ('Карта потеряна', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5043: ('Карта украдена', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5051: ('Недостаточно средств', 'Недостаточно средств на карте'),
    5054: ('Карта просрочена или неверно указан срок действия', 
           'Проверьте правильность введенных данных карты или воспользуйтесь ' +
           'другой картой'),
    5057: ('Ограничение на карте', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5065: ('Превышен лимит операций по карте', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5075: ('Превышено количество неправильных вводов PIN',
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5082: ('Неверный CVV код', 'Неверно указан код CVV'),
    5091: ('Эмитент недоступен', 
           'Повторите попытку позже или воспользуйтесь другой картой'),
    5092: ('Эмитент недоступен', 
           'Повторите попытку позже или воспользуйтесь другой картой'),
    5096: ('Ошибка банка-эквайера или сети', 'Повторите попытку позже'),
    5204: ('Операция не может быть обработана по прочим причинам', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5206: ('3-D Secure авторизация не пройдена', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5207: ('3-D Secure авторизация недоступна',
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5209: ('3-D Secure авторизация недоступна', 
           'Свяжитесь с вашим банком или воспользуйтесь другой картой'),
    5300: ('Лимиты эквайера на проведение операций', 
           'Воспользуйтесь другой картой')
}


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


class ReceiptType(object):
    INCOME = 'Income'
    INCOME_RETURN = 'IncomeReturn'
    EXPENSE = 'Expense'
    EXPENSE_RETURN = 'ExpenseReturn'


class TaxationSystem(object):
    OSNO = 0
    USN_INCOME = 1
    USN_INCOME_MINUS_EXPENSES = 2
    ENVD = 3
    ESHN = 4
    PSN = 5


class VAT(object):
    """Vat options according to CloudPayaments docs.

    https://cloudpayments.ru/wiki/integration/instrumenti/apikassa#nds
    """

    WITHOUT = None  # null или не указано — НДС не облагается
    VAT20 = 20  # НДС 20%
    VAT18 = 18  # НДС 18%
    VAT10 = 10  # НДС 10%
    VAT0 = 0  # НДС 0%
    VAT110 = 110  # расчетный НДС 10/110
    VAT118 = 118  # расчетный НДС 18/118
    VAT120 = 120  # расчетный НДС 20/120
