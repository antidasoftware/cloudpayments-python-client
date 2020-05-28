# coding=utf-8
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
    """Receipt model representation."""

    def __init__(self, items, taxation_system, email='', phone='', amounts=None):
        self.items = items
        self.taxation_system = taxation_system
        self.email = email
        self.phone = phone
        self.amounts = amounts

    @classmethod
    def from_dict(cls, receipt_dict):
        """Retrieve data from dict and place it as object properties."""
        items = [ReceiptItem.from_dict(item) for item in receipt_dict['Items']]
        amounts_dict = receipt_dict.get('Amounts', None)
        amounts = Amount.from_dict(amounts_dict) if amounts_dict else None
        return cls(items=items,
                   taxation_system=receipt_dict.get('TaxationSystem'),
                   email=receipt_dict.get('Email'),
                   phone=receipt_dict.get('Phone'),
                   amounts=amounts)

    def to_dict(self):
        """Convert instance properties to dict."""
        items = [item.to_dict() for item in self.items]
        result = {
            'items': items,
            'taxationSystem': self.taxation_system,
            'email': self.email,
            'phone': self.phone,
        }
        if isinstance(self.amounts, Amount):
            result.update({'Amounts': self.amounts.to_dict()})
        return result


class Amount(Model):
    """Amount model representation."""

    def __init__(self, electronic=None, advance_payment=None, credit=None, provision=None):
        """Initial method."""
        self.electronic = electronic  # Сумма оплаты электронными деньгами
        self.advance_payment = advance_payment  # Сумма из предоплаты (зачетом аванса) (2 знака после запятой)
        self.credit = credit  # Сумма постоплатой(в кредит) (2 знака после запятой)
        self.provision = provision  # Сумма оплаты встречным предоставлением (сертификаты, др. мат.ценности) (2 знака после запятой)

    def to_dict(self):
        """Convert instance properties to dict."""
        return {
            'electronic': self.electronic,
            'advancePayment': self.advance_payment,
            'credit': self.credit,
            'provision': self.provision
        }

    @classmethod
    def from_dict(cls, amount_dict):
        """Retrieve data from dict and place it as object properties."""
        return cls(
            electronic=amount_dict.get('Electronic'),
            advance_payment=amount_dict.get('AdvancePayment'),
            credit=amount_dict.get('Credit'),
            provision=amount_dict.get('Provision')
        )


class ReceiptItem(Model):
    """Receipt Item model representation."""

    def __init__(self, label, price, quantity, amount, vat, ean13=None,
                 method=0, item_object=0, measurement_unit=None):
        """Initial method."""
        self.label = label
        self.price = price
        self.quantity = quantity
        self.amount = amount
        self.vat = vat  # Propety of enums.VAT
        self.ean13 = ean13
        self.method = method  # признак способа расчета
        self.item_object = item_object  # признак предмета товара, работы, услуги, платежа, выплаты, иного предмета расчета
        self.measurement_unit = measurement_unit  # единица измерения

    @classmethod
    def from_dict(cls, item_dict):
        """Retrieve data from dict and place it as object properties."""
        return cls(label=item_dict.get('Label'),
                   price=item_dict.get('Price'),
                   quantity=item_dict.get('Quantity'),
                   amount=item_dict.get('Amount'),
                   vat=item_dict.get('Vat'),
                   ean13=item_dict.get('EAN13'),
                   measurement_unit=item_dict.get('MeasurementUnit'),
                   item_object=item_dict.get('Object'),
                   method=item_dict.get('Method'))

    def to_dict(self):
        """Convert instance properties to dict."""
        return {
            'label': self.label,
            'price': self.price,
            'quantity': self.quantity,
            'amount': self.amount,
            'vat': self.vat,
            'ean13': self.ean13,
            'method': self.method,
            'object': self.item_object,
            'measurementUnit': self.measurement_unit
        }
