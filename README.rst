===================================
CloudPayments Python Client Library
===================================

.. image:: https://img.shields.io/pypi/v/cloudpayments.svg
   :target: https://pypi.python.org/pypi/cloudpayments/
   :alt: Python Package Index

.. image:: https://img.shields.io/travis/antidasoftware/cloudpayments-python-client.svg
   :target: https://travis-ci.org/antidasoftware/cloudpayments-python-client
   :alt: Travis CI

Клиент для платежного сервиса `CloudPayments <http://cloudpayments.ru/>`_. Позволяет обращаться к `API CloudPayments <http://cloudpayments.ru/Docs/Api>`_ из кода на Python.

Установка
=========

::

    pip install cloudpayments


Требования
==========

Python 2.7 или 3.4+


Использование
=============

.. code:: python

    from cloudpayments import CloudPayments

    client = CloudPayments('public_id', 'api_secret')
    client.test()

При создании клиента задаются аутентификационные параметры: Public ID и Api Secret. Оба этих значения можно получить в личном кабинете.

Обращение к API осуществляется через методы клиента.


| **Тестовый метод** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#test>`__)

.. code:: python

    test(self, request_id=None)

``request_id`` — идентификатор для `идемпотентного запроса <https://developers.cloudkassir.ru/#idempotentnost-api>`__.

В случае успеха возвращает строку с сообщением от сервиса.


| **Оплата по криптограмме** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#pay_with_crypto>`__)

.. code:: python

    charge_card(self, cryptogram, amount, currency, name, ip_address,
                invoice_id=None, description=None, account_id=None,
                email=None, data=None, require_confirmation=False,
                service_fee=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``data`` — произвольные данные, при отправке будут сериализованы в JSON.

``service_fee`` — сервисный сбор.

``require_confirmation`` — если установлено в ``True``, платеж будет выполняться по двухстадийной схеме.

В случае успеха возвращает объект типа ``Transaction`` (если не требуется 3-D Secure аутентификация) либо ``Secure3d`` (если требуется).


| **Завершение оплаты после прохождения 3-D Secure** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#3ds>`__)

.. code:: python

    finish_3d_secure_authentication(self, transaction_id, pa_res)

В случае успеха возвращает объект типа ``Transaction``.


| **Оплата по токену** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#paywithtoken>`__)

.. code:: python

    charge_token(self, token, account_id, amount, currency,
                 ip_address=None, invoice_id=None, description=None,
                 email=None, data=None, require_confirmation=False)

``currency`` — одна из констант, определенных в классе ``Currency``

``data`` — произвольные данные, при отправке будут сериализованы в JSON.

``require_confirmation`` — если установлено в ``True``, платеж будет выполняться по двухстадийной схеме.

В случае успеха возвращает объект типа ``Transaction``.


| **Подтверждение оплаты** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#approval>`__)

.. code:: python

    confirm_payment(self, transaction_id, amount, data=None)

``data`` — произвольные данные, при отправке будут сериализованы в JSON.

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Отмена оплаты** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#void>`__)

.. code:: python

    void_payment(self, transaction_id)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Возврат денег** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#refund>`__)

.. code:: python

    refund(self, transaction_id, amount, request_id=None)

``request_id`` — идентификатор для `идемпотентного запроса <https://developers.cloudkassir.ru/#idempotentnost-api>`__.

В случае успеха возвращает идентификатор транзакции возврата.


| **Выплата по токену** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#payment_token>`__)

.. code:: python
    
    topup(self, token, amount, account_id, currency, invoice_id=None)

``currency`` — одна из констант, определенных в классе ``Currency``

В случае успеха возвращает объект типа ``Transaction``.


| **Получение транзакции** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#oper_info>`__)

.. code:: python

    get_transaction(self, transaction_id)

``transaction_id`` — ID транзакции

В случае успеха возвращает объект типа ``Transaction``.


| **Проверка статуса платежа** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#status_check>`__)

.. code:: python

    find_payment(self, invoice_id)

В случае успеха возвращает объект типа ``Transaction``.


| **Выгрузка списка транзакций** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#oper_load>`__)

.. code:: python

    list_payments(self, date, timezone=None)

``date`` — объект типа ``datetime.date``.

``timezone`` — одна из констант, определенных в классе ``Timezone``.

В случае успеха возвращает список объектов типа ``Transaction``.


| **Создание подписки** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#create_recurrent>`__)

.. code:: python

    create_subscription(self, token, account_id, amount, currency,
                        description, email, start_date, interval, period,
                        require_confirmation=False, max_periods=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``start_date`` — объект типа ``datetime.datetime``.

``interval`` — одна из констант, определенных в классе ``Interval``.

В случае успеха возвращает объект типа ``Subscription``.


| **Выгрузка списка подписок** (`описание <https://developers.cloudpayments.ru/#poisk-podpisok>`__)

.. code:: python

    list_subscriptions(self, account_id)
    
``account_id`` — идентификатор пользователя.

В случае успеха возвращает список объектов типа ``Subscription``.


| **Запрос статуса подписки** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#rec_info>`__)

.. code:: python

    get_subscription(self, subscription_id)

В случае успеха возвращает объект типа ``Subscription``.


| **Изменение подписки** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#rec_change>`__)

.. code:: python

    update_subscription(self, subscription_id, amount=None, currency=None,
                        description=None, start_date=None, interval=None,
                        period=None, require_confirmation=None,
                        max_periods=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``start_date`` — объект типа ``datetime.datetime``.

``interval`` — одна из констант, определенных в классе ``Interval``.

В случае успеха возвращает объект типа ``Subscription``.


| **Отмена подписки** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#rec_cancel>`__)

.. code:: python

    cancel_subscription(self, subscription_id)

В случае успеха метод ничего не возвращает, при ошибке бросает исключение.


| **Отправка счета по почте** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#create_invoice>`__)

.. code:: python

    create_order(self, amount, currency, description, email=None,
                 send_email=None, require_confirmation=None,
                 invoice_id=None, account_id=None, phone=None,
                 send_sms=None, send_whatsapp=None, culture_info=None)

``currency`` — одна из констант, определенных в классе ``Currency``.

``culture_info`` — одна из констант, определенных в классе ``CultureInfo``.

В случае успеха возвращает объект типа ``Order``.


| **Формирование кассового чека** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/apikassa#form>`__)

.. code:: python

    create_receipt(self, inn, receipt_type, customer_receipt, 
                   invoice_id=None, account_id=None, request_id=None)

``receipt_type`` — одна из констант, определенных в классе ``ReceiptType``.

``customer_receipt`` — объект типа ``Receipt`` или словарь с данными чека.

``request_id`` — идентификатор для `идемпотентного запроса <https://developers.cloudkassir.ru/#idempotentnost-api>`__.

В случае успеха возвращает строку с уникальным идентификатором чека.


| **Получение данных чека** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/apikassa#Получение%20данных%20чека>`__)

.. code:: python

    get_receipt(self, receipt_id)


``receipt_id`` — идентификатор чека

В случае успеха возвращает объект типа ``Receipt``

Авторы
======

Разработано в `Antida software <http://antidasoftware.com>`_.
Мы создаем SaaS-продукты и сервисы, интегрированные с платежными системами.
Пишите нам, если вам нужна консультация по работе с биллинговыми системами: `info@antidasoftware.com <info@antidasoftware.com>`_.


Лицензия
========

MIT
