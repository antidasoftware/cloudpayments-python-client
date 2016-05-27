from datetime import datetime
import pytz


def parse_datetime(s):
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
                   transaction_dict['Token']
        )


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
                   secure3d_dict['AcsUrl']
        )