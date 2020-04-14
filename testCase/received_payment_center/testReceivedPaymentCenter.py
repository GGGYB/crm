# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
import sys
from decimal import Decimal as D
from commons import common
from commons.const import const
from commons import filters
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid
from .testAddReceivedPayments import AddReceivedPayment
from .testGetReceivedPayments import GetReceivedPayments
from .testDeleteReceivedPayments import DeleteReceivedPayments
from .testUpdateReceivedPayments import UpdateReceivedPayments
class ReceivedPaymentCenter:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.add_received_payments = AddReceivedPayment(cookie, csrf)
        self.get_received_payments = GetReceivedPayments(cookie, csrf)
        self.update_received_payments = UpdateReceivedPayments(cookie, csrf)
        self.delete_received_payments = DeleteReceivedPayments(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.user_id = ''
        self.customers_id = []
        self.params = ''
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        pass

    def testReceivedPaymentCenter(self):
        self.testReceivedPaymentPlans()
        self.testReceivedPayments()
        self.testInvoiceddPayments()

    ##回款计划
    def testReceivedPaymentPlans(self):
        self.add_received_payments.add_received_payment_plans()
        scopes = self.get_received_payments.get_received_payment_plans_scope()
        self.filters.receive_payments_filters_by_business('ReceivedPaymentsCenter', scopes)
        for scope in scopes:
            self.testDeleteReceivedPayments(scope)

    
    ##回款记录
    def testReceivedPayments(self):
        self.add_received_payments.add_received_payments()
        scopes = self.get_received_payments.get_received_payment_scope()
        self.filters.receive_payments_filters_by_business('ReceivedPaymentsCenter', scopes)
        for scope in scopes:
            self.testDeleteReceivedPayments(scope)

    ##开票记录
    def testInvoiceddPayments(self):
        self.add_received_payments.add_invoiced_payments()
        scopes = self.get_received_payments.get_invoiced_payments_scope()
        self.filters.receive_payments_filters_by_business('ReceivedPaymentsCenter', scopes)
        for scope in scopes:
            self.testDeleteReceivedPayments(scope)

    def testDeleteReceivedPayments(self, scope):
        received_payments_ids = []
        received_payment_plans_ids = []

        for i in range(5):
            received_payment_plans_ids.append(self.add_received_payments.add_received_payment_plans())
            if i < 2:
                self.delete_received_payments.delete_received_payment_plans(received_payment_plans_ids[0])
                received_payment_plans_ids.remove(received_payment_plans_ids[0])
        self.delete_received_payments.delete_received_payments(scope, received_payments_ids)
        for i in range(5):
            received_payments_ids.append(self.add_received_payments.add_received_payments())
            if i < 2:
                self.delete_received_payments.delete_received_payments(received_payments_ids[0])
                received_payments_ids.remove(received_payments_ids[0])
        self.delete_received_payments.delete_received_payments(scope, received_payments_ids)