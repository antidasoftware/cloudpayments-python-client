from datetime import datetime
import pytz


def parse_datetime(s):
    if not s:
        return None
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)


class Transaction(object):
    def __init__(self, id, amount, currency, currency_code, invoice_id,
                 account_id, email, description, data, created_date,
                 auth_date, confirm_date, auth_code, test_mode, ip_address,
                 ip_country, ip_city, ip_region, ip_district, ip_latitude,
                 ip_longitude, card_first_six, card_last_four, card_exp_date,
                 card_type, card_type_code, issuer, issuer_bank_country,
                 status, status_code, reason, reason_code, cardholder_message,
                 name, token):
        self.id = id
        self.amount = amount
        self.currency = currency
        self.currency_code = currency_code
        self.invoice_id = invoice_id
        self.account_id = account_id
        self.email = email
        self.description = description
        self.data = data
        self.created_date = created_date
        self.auth_date = auth_date
        self.confirm_date = confirm_date
        self.auth_code = auth_code
        self.test_mode = test_mode
        self.ip_address = ip_address
        self.ip_country = ip_country
        self.ip_city = ip_city
        self.ip_region = ip_region
        self.ip_district = ip_district
        self.ip_latitude = ip_latitude
        self.ip_longitude = ip_longitude
        self.card_first_six = card_first_six
        self.card_last_four = card_last_four
        self.card_exp_date = card_exp_date
        self.card_type = card_type
        self.card_type_code = card_type_code
        self.issuer = issuer
        self.issuer_bank_country = issuer_bank_country
        self.status = status
        self.status_code = status_code
        self.reason = reason
        self.reason_code = reason_code
        self.cardholder_message = cardholder_message
        self.name = name
        self.token = token

    @classmethod
    def from_dict(cls, transaction_dict):
        return cls(transaction_dict['TransactionId'],
                   transaction_dict['Amount'],
                   transaction_dict['Currency'],
                   transaction_dict['CurrencyCode'],
                   transaction_dict['InvoiceId'],
                   transaction_dict['AccountId'],
                   transaction_dict['Email'],
                   transaction_dict['Description'],
                   transaction_dict['JsonData'],
                   parse_datetime(transaction_dict['CreatedDateIso']),
                   parse_datetime(transaction_dict['AuthDateIso']),
                   parse_datetime(transaction_dict['ConfirmDateIso']),
                   transaction_dict['AuthCode'],
                   transaction_dict['TestMode'],
                   transaction_dict['IpAddress'],
                   transaction_dict['IpCountry'],
                   transaction_dict['IpCity'],
                   transaction_dict['IpRegion'],
                   transaction_dict['IpDistrict'],
                   transaction_dict['IpLatitude'],
                   transaction_dict['IpLongitude'],
                   transaction_dict['CardFirstSix'],
                   transaction_dict['CardLastFour'],
                   transaction_dict['CardExpDate'],
                   transaction_dict['CardType'],
                   transaction_dict['CardTypeCode'],
                   transaction_dict['Issuer'],
                   transaction_dict['IssuerBankCountry'],
                   transaction_dict['Status'],
                   transaction_dict['StatusCode'],
                   transaction_dict['Reason'],
                   transaction_dict['ReasonCode'],
                   transaction_dict['CardHolderMessage'],
                   transaction_dict['Name'],
                   transaction_dict['Token'])


class Secure3d(object):
    def __init__(self, transaction_id, pa_req, acs_url):
        self.transaction_id = transaction_id
        self.pa_req = pa_req
        self.acs_url = acs_url

    def redirect_url(self, term_url):
        return '%s?MD=%s&PaReq=%s&TermUrl=%s' % (
            self.acs_url, self.transaction_id, self.pa_req, term_url
        )

    @classmethod
    def from_dict(cls, secure3d_dict):
        return cls(secure3d_dict['TransactionId'],
                   secure3d_dict['PaReq'],
                   secure3d_dict['AcsUrl'])


class Subscription(object):
    def __init__(self, id, account_id, description, email, amount,
                 currency_code, currency, require_confirmation, start_date,
                 interval_code, interval, period, max_periods, status_code,
                 status, successful_transactions_number,
                 failed_transactions_number, last_transaction_date,
                 next_transaction_date):
        self.id = id
        self.account_id = account_id
        self.description = description
        self.email = email
        self.amount = amount
        self.currency_code = currency_code
        self.currency = currency
        self.require_confirmation = require_confirmation
        self.start_date = start_date
        self.interval_code = interval_code
        self.interval = interval
        self.period = period
        self.max_periods = max_periods
        self.status_code = status_code
        self.status = status
        self.successful_transactions_number = successful_transactions_number
        self.failed_transactions_number = failed_transactions_number
        self.last_transaction_date = last_transaction_date
        self.next_transaction_date = next_transaction_date

    @classmethod
    def from_dict(cls, subscription_dict):
        return cls(subscription_dict['Id'],
                   subscription_dict['AccountId'],
                   subscription_dict['Description'],
                   subscription_dict['Email'],
                   subscription_dict['Amount'],
                   subscription_dict['CurrencyCode'],
                   subscription_dict['Currency'],
                   subscription_dict['RequireConfirmation'],
                   parse_datetime(subscription_dict['StartDateIso']),
                   subscription_dict['IntervalCode'],
                   subscription_dict['Interval'],
                   subscription_dict['Period'],
                   subscription_dict['MaxPeriods'],
                   subscription_dict['StatusCode'],
                   subscription_dict['Status'],
                   subscription_dict['SuccessfulTransactionsNumber'],
                   subscription_dict['FailedTransactionsNumber'],
                   parse_datetime(subscription_dict['LastTransactionDateIso']),
                   parse_datetime(subscription_dict['NextTransactionDateIso']))


class Order(object):
    def __init__(self, id, number, amount, currency, currency_code, email,
                 description, require_confirmation, url):
        self.id = id
        self.number = number
        self.amount = amount
        self.currency = currency
        self.currency_code = currency_code
        self.email = email
        self.description = description
        self.require_confirmation = require_confirmation
        self.url = url

    @classmethod
    def from_dict(cls, order_dict):
        return cls(order_dict['Id'],
                   order_dict['Number'],
                   order_dict['Amount'],
                   order_dict['Currency'],
                   order_dict['CurrencyCode'],
                   order_dict['Email'],
                   order_dict['Description'],
                   order_dict['RequireConfirmation'],
                   order_dict['Url'])