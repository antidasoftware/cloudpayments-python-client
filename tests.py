# coding=utf-8
from datetime import datetime
import json
from unittest import TestCase
import pytz

from models import parse_datetime, Transaction
from enums import Currency, TransactionStatus, ReasonCode


class ParseDateTimeTest(TestCase):
    def test_parses_datetime(self):
        self.assertEqual(parse_datetime('2014-08-09T11:49:42'),
                         datetime(2014, 8, 9, 11, 49, 42, tzinfo=pytz.utc))


class TransactionTest(TestCase):
    def test_reads_transaction_from_dict(self):
        model = json.loads(u'''{
            "TransactionId": 504,
            "Amount": 10.00000,
            "Currency": "RUB",
            "CurrencyCode": 0,
            "InvoiceId": "1234567",
            "AccountId": "user_x",
            "Email": null,
            "Description": "Оплата товаров в example.com",
            "JsonData": {"key": "value"},
            "CreatedDate": "\/Date(1401718880000)\/",
            "CreatedDateIso":"2014-08-09T11:49:41",
            "AuthDate": "\/Date(1401733880523)\/",
            "AuthDateIso":"2014-08-09T11:49:42",
            "ConfirmDate": "\/Date(1401733880523)\/",
            "ConfirmDateIso":"2014-08-09T11:49:42",
            "AuthCode": "123456",
            "TestMode": true,
            "IpAddress": "195.91.194.13",
            "IpCountry": "RU",
            "IpCity": "Уфа",
            "IpRegion": "Республика Башкортостан",
            "IpDistrict": "Приволжский федеральный округ",
            "IpLatitude": 54.7355,
            "IpLongitude": 55.991982,
            "CardFirstSix": "411111",
            "CardLastFour": "1111",
            "CardExpDate": "05/19",
            "CardType": "Visa",
            "CardTypeCode": 0,
            "Issuer": "Sberbank of Russia",
            "IssuerBankCountry": "RU",
            "Status": "Completed",
            "StatusCode": 3,
            "Reason": "Approved",
            "ReasonCode": 0,
            "CardHolderMessage":"Оплата успешно проведена",
            "Name": "CARDHOLDER NAME",
            "Token": "a4e67841-abb0-42de-a364-d1d8f9f4b3c0"
        }''')
        transaction = Transaction.from_dict(model)
        self.assertEqual(transaction.id, 504)
        self.assertEqual(transaction.amount, 10)
        self.assertEqual(transaction.currency, Currency.RUB)
        self.assertEqual(transaction.currency_code, 0)
        self.assertEqual(transaction.invoice_id, '1234567')
        self.assertEqual(transaction.account_id, 'user_x')
        self.assertEqual(transaction.email, None)
        self.assertEqual(transaction.description,
                         u'Оплата товаров в example.com')
        self.assertEqual(transaction.data, {'key': 'value'})
        self.assertEqual(transaction.created_date,
                         datetime(2014, 8, 9, 11, 49, 41, tzinfo=pytz.utc))
        self.assertEqual(transaction.auth_date,
                         datetime(2014, 8, 9, 11, 49, 42, tzinfo=pytz.utc))
        self.assertEqual(transaction.confirm_date,
                         datetime(2014, 8, 9, 11, 49, 42, tzinfo=pytz.utc))
        self.assertEqual(transaction.auth_code, '123456')
        self.assertTrue(transaction.test_mode)
        self.assertEqual(transaction.ip_address, '195.91.194.13')
        self.assertEqual(transaction.ip_country, 'RU')
        self.assertEqual(transaction.ip_city, u'Уфа')
        self.assertEqual(transaction.ip_region, u'Республика Башкортостан')
        self.assertEqual(transaction.ip_district,
                         u'Приволжский федеральный округ')
        self.assertEqual(transaction.ip_latitude, 54.7355)
        self.assertEqual(transaction.ip_longitude, 55.991982)
        self.assertEqual(transaction.card_first_six, '411111')
        self.assertEqual(transaction.card_last_four, '1111')
        self.assertEqual(transaction.card_exp_date, '05/19')
        self.assertEqual(transaction.card_type, 'Visa')
        self.assertEqual(transaction.card_type_code, 0)
        self.assertEqual(transaction.issuer, 'Sberbank of Russia')
        self.assertEqual(transaction.issuer_bank_country, 'RU')
        self.assertEqual(transaction.status, TransactionStatus.COMPLETED)
        self.assertEqual(transaction.status_code, 3)
        self.assertEqual(transaction.reason, 'Approved')
        self.assertEqual(transaction.reason_code, ReasonCode.APPROVED)
        self.assertEqual(transaction.cardholder_message,
                         u'Оплата успешно проведена')
        self.assertEqual(transaction.name, 'CARDHOLDER NAME')
        self.assertEqual(transaction.token,
                         'a4e67841-abb0-42de-a364-d1d8f9f4b3c0')



