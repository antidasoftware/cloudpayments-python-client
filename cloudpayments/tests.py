# coding=utf-8
from datetime import datetime, date
import json
from unittest import TestCase

import pytz

from .models import Transaction, Secure3d, Subscription, Order
from .utils import parse_datetime, format_datetime, format_date
from .enums import Currency, TransactionStatus, ReasonCode, Interval, \
    SubscriptionStatus


class ParseDateTimeTest(TestCase):
    def test_parses_datetime(self):
        self.assertEqual(parse_datetime('2014-08-09T11:49:42'),
                         datetime(2014, 8, 9, 11, 49, 42, tzinfo=pytz.utc))


class FormatDateTimeTest(TestCase):
    def test_formats_datetime(self):
        dt = datetime(2016, 8, 9, 11, 49, 42, tzinfo=pytz.utc)
        self.assertEqual(format_datetime(dt), '2016-08-09T11:49:42')

    def test_formats_local_datetime(self):
        timezone = pytz.timezone('Europe/Moscow')
        dt = timezone.localize(datetime(2016, 8, 9, 14, 49, 42))
        self.assertEqual(format_datetime(dt), '2016-08-09T11:49:42')


class FormatDateTest(TestCase):
    def test_formats_date(self):
        d = date(2016, 8, 9)
        self.assertEqual(format_date(d), '2016-08-09')


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


class Secure3dTest(TestCase):
    def test_reads_secure3d_from_dict(self):
        model = json.loads(u'''{
            "TransactionId": 504,
            "PaReq": "eJxVUdtugkAQ/RXDe9mLgo0Z1nhpU9PQasWmPhLYAKksuEChfn13uVR9mGTO7MzZM2dg3qSn0Q+X\\nRZIJxyAmNkZcBFmYiMgxDt7zw6MxZ+DFkvP1ngeV5AxcXhR+xEdJ6BhpEZnEYLBdfPAzg56JKSKT\\nAhqgGpFB7IuSgR+cl5s3NqFTG2NAPYSUy82aETqeWPYUUAdB+ClnwSmrwtz/TbkoC0BtDYKsEqX8\\nZfZkDGgAUMkTi8synyFU17V5N2nKCpBuAHRVs610VijCJgmZu17UXTxhFWP34l7evYPlegsHkO6A\\n0C85o5hMsI3piNIZHc+IBaitg59qJYzgdrUOQK7/WNy+3FZAeSqV5cMqAwLe5JlQwpny8T8HdFW8\\netFuBqUyahV+Hjf27vWCaSx22fe+KY6kXKZfJLK1x22TZkyUS8QiHaUGgDQN6s+H+tOq7O7kf8hd\\nt30=",
            "AcsUrl": "https://test.paymentgate.ru/acs/auth/start.do"
        }''')
        secure3d = Secure3d.from_dict(model)

        self.assertEqual(secure3d.transaction_id, 504)
        self.assertEqual(secure3d.pa_req, 'eJxVUdtugkAQ/RXDe9mLgo0Z1nhpU9PQasWmPhLYAKksuEChfn13uVR9mGTO7MzZM2dg3qSn0Q+X\nRZIJxyAmNkZcBFmYiMgxDt7zw6MxZ+DFkvP1ngeV5AxcXhR+xEdJ6BhpEZnEYLBdfPAzg56JKSKT\nAhqgGpFB7IuSgR+cl5s3NqFTG2NAPYSUy82aETqeWPYUUAdB+ClnwSmrwtz/TbkoC0BtDYKsEqX8\nZfZkDGgAUMkTi8synyFU17V5N2nKCpBuAHRVs610VijCJgmZu17UXTxhFWP34l7evYPlegsHkO6A\n0C85o5hMsI3piNIZHc+IBaitg59qJYzgdrUOQK7/WNy+3FZAeSqV5cMqAwLe5JlQwpny8T8HdFW8\netFuBqUyahV+Hjf27vWCaSx22fe+KY6kXKZfJLK1x22TZkyUS8QiHaUGgDQN6s+H+tOq7O7kf8hd\nt30=')
        self.assertEqual(secure3d.acs_url,
                         'https://test.paymentgate.ru/acs/auth/start.do')

    def test_builds_redirect_params(self):
        secure3d = Secure3d(111, 'asdas',
                            'https://test.paymentgate.ru/acs/auth/start.do')
        self.assertEqual(
            secure3d.redirect_params('http://example.com'),
            {'MD': 111, 'PaReq': 'asdas', 'TermUrl': 'http://example.com'}
        )


class SubscriptionTest(TestCase):
    def test_reads_subscription_from_dict(self):
        model = json.loads(u'''{
            "Id":"sc_8cf8a9338fb8ebf7202b08d09c938",
            "AccountId":"user@example.com",
            "Description":"Ежемесячная подписка на сервис example.com",
            "Email":"user@example.com",
            "Amount":1.02,
            "CurrencyCode":0,
            "Currency":"RUB",
            "RequireConfirmation":false,
            "StartDate":"\/Date(1407343589537)\/",
            "StartDateIso":"2014-08-09T11:49:41",
            "IntervalCode":1,
            "Interval":"Month",
            "Period":1,
            "MaxPeriods":null,
            "StatusCode":0,
            "Status":"Active",
            "SuccessfulTransactionsNumber":0,
            "FailedTransactionsNumber":0,
            "LastTransactionDate":null,
            "LastTransactionDateIso":null,
            "NextTransactionDate":"\/Date(1407343589537)\/",
            "NextTransactionDateIso":"2014-08-09T11:49:41"
        }''')
        subscription = Subscription.from_dict(model)
        self.assertEqual(subscription.id, 'sc_8cf8a9338fb8ebf7202b08d09c938')
        self.assertEqual(subscription.account_id, 'user@example.com')
        self.assertEqual(subscription.description,
                         u'Ежемесячная подписка на сервис example.com')
        self.assertEqual(subscription.email, 'user@example.com')
        self.assertEqual(subscription.amount, 1.02)
        self.assertEqual(subscription.currency_code, 0)
        self.assertEqual(subscription.currency, Currency.RUB)
        self.assertFalse(subscription.require_confirmation)
        self.assertEqual(subscription.start_date,
                         datetime(2014, 8, 9, 11, 49, 41, tzinfo=pytz.utc))
        self.assertEqual(subscription.interval_code, 1)
        self.assertEqual(subscription.interval, Interval.MONTH)
        self.assertEqual(subscription.period, 1)
        self.assertEqual(subscription.max_periods, None)
        self.assertEqual(subscription.status_code, 0)
        self.assertEqual(subscription.status, SubscriptionStatus.ACTIVE)
        self.assertEqual(subscription.successful_transactions_number, 0)
        self.assertEqual(subscription.failed_transactions_number, 0)
        self.assertEqual(subscription.last_transaction_date, None)
        self.assertEqual(subscription.next_transaction_date,
                         datetime(2014, 8, 9, 11, 49, 41, tzinfo=pytz.utc))


class OrderTest(TestCase):
    def test_reads_order_from_dict(self):
        model = json.loads('''{
            "Id":"f2K8LV6reGE9WBFn",
            "Number":61,
            "Amount":10.0,
            "Currency":"RUB",
            "CurrencyCode":0,
            "Email":"client@test.local",
            "Description":"Оплата на сайте example.com",
            "RequireConfirmation":true,
            "Url":"https://orders.cloudpayments.ru/d/f2K8LV6reGE9WBFn"
        }''')
        order = Order.from_dict(model)

        self.assertEqual(order.id, 'f2K8LV6reGE9WBFn')
        self.assertEqual(order.number, 61)
        self.assertEqual(order.amount, 10.0)
        self.assertEqual(order.currency, Currency.RUB)
        self.assertEqual(order.currency_code, 0)
        self.assertEqual(order.email, 'client@test.local')
        self.assertEqual(order.description, u'Оплата на сайте example.com')
        self.assertTrue(order.require_confirmation)
        self.assertEqual(order.url,
                         u'https://orders.cloudpayments.ru/d/f2K8LV6reGE9WBFn')
