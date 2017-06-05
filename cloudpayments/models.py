from .utils import parse_datetime


class Model(object):
    @classmethod
    def from_dict(cls, model_dict):
        raise NotImplementedError

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))


class Transaction(Model):
    def __init__(self, id, amount, currency, currency_code, invoice_id,
                 account_id, email, description, data, created_date,
                 auth_date, confirm_date, auth_code, test_mode, ip_address,
                 ip_country, ip_city, ip_region, ip_district, ip_latitude,
                 ip_longitude, card_first_six, card_last_four, card_exp_date,
                 card_type, card_type_code, issuer, issuer_bank_country,
                 status, status_code, reason, reason_code, cardholder_message,
                 name, token):
        super(Transaction, self).__init__()
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

    @property
    def secure3d_required(self):
        return False

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


class Secure3d(Model):
    def __init__(self, transaction_id, pa_req, acs_url):
        super(Secure3d, self).__init__()
        self.transaction_id = transaction_id
        self.pa_req = pa_req
        self.acs_url = acs_url

    @property
    def secure3d_required(self):
        return True

    def redirect_params(self, term_url):
        return {'MD': self.transaction_id,
                'PaReq': self.pa_req,
                'TermUrl': term_url}

    @classmethod
    def from_dict(cls, secure3d_dict):
        return cls(secure3d_dict['TransactionId'],
                   secure3d_dict['PaReq'],
                   secure3d_dict['AcsUrl'])


class Subscription(Model):
    def __init__(self, id, account_id, description, email, amount,
                 currency_code, currency, require_confirmation, start_date,
                 interval_code, interval, period, max_periods, status_code,
                 status, successful_transactions_number,
                 failed_transactions_number, last_transaction_date,
                 next_transaction_date):
        super(Subscription, self).__init__()
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


class Order(Model):
    def __init__(self, id, number, amount, currency, currency_code, email,
                 description, require_confirmation, url):
        super(Order, self).__init__()
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


class Receipt(Model):
    def __init__(self, items, taxation_system, email='', phone=''):
        self.items = items
        self.taxation_system = taxation_system
        self.email = email
        self.phone = phone

    @classmethod
    def from_dict(cls, receipt_dict):
        items = [ReceiptItem.from_dict(item) for item in receipt_dict['Items']]
        return cls(items,
                   receipt_dict['taxationSystem'],
                   receipt_dict['email'],
                   receipt_dict['phone'])
    
    def to_dict(self):
        items = [item.to_dict() for item in self.items]
        return {
            'items': items,
            'taxationSystem': self.taxation_system,
            'email': self.email,
            'phone': self.phone
        }


class ReceiptItem(Model):
    def __init__(self, label, price, quantity, amount, vat, ean13=None):
        self.label = label
        self.price = price
        self.quantity = quantity
        self.amount = amount
        self.vat = vat
        self.ean13 = ean13

    @classmethod
    def from_dict(cls, item_dict):
        return cls(item_dict['label'],
                   item_dict['price'],
                   item_dict['quantity'],
                   item_dict['amount'],
                   item_dict['vat'],
                   item_dict.get('ean13'))
    
    def to_dict(self):
        return {
            'label': self.label,
            'price': self.price,
            'quantity': self.quantity,
            'amount': self.amount,
            'vat': self.vat,
            'ean13': self.ean13
        }