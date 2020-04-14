# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

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
from .testSettingsCustomerApprovals import Approvals
from .testAddCustomer import AddCustomer
from .testGetCustomer import GetCustomers
from .testUpdateCustomer import UpdateCustomer
from .testDeleteCustomer import DeleteCustomer

class Customers:
    def __init__(self, cookie, csrf):
        #'https://e.ikcrm.com/
        # self.base_url = base_url
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.add = AddCustomer(cookie, csrf)
        self._get_customer = GetCustomers(cookie, csrf)
        self._update_customer = UpdateCustomer(cookie, csrf)
        self._delete_customer = DeleteCustomer(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def testCustomers(self):
        self.testAddCustomer()
        # self.testApprovalCustomer() 客户审批暂不执行
        scopes = self._get_customer.customers_get_scopes()
        self.testGetCustomers(scopes)
        self.testUpdateCustomers(scopes)
        self.testCloseCustomersApprovals()
        self.testDeleteCustomers()

    def testAddCustomer(self):
        self.testOpenCustomersApprovals()
        self.applying_customer = self.add.add_applying_customer()
        self.testCloseCustomersApprovals()
        self.customer = self.add.add_customers()
        self.testCloseCustomersApprovals()

    def testGetCustomers(self, scopes):
        self.testCloseCustomersApprovals()
        self.filters.filters_by_business('customers', scopes)
        customer_id = self.add.add_customers()
        self._get_customer.customer(customer_id)
        self._get_customer.customers_dulicate('1111')

    #编辑客户
    def testUpdateCustomers(self, scopes):
        for scope in scopes:
            customer_ids = []
            for i in range(3):
                customer_ids.append(self.add.add_customers())
            self._update_customer.update_customers_by_scope(scope, customer_ids)

    #删除客户
    def testDeleteCustomers(self):
        #删除单个客户
        customer_id = self.add.add_customers()
        self._delete_customer.delete_customer(customer_id)
        #批量删除客户
        customer_ids = []
        for i in range(2):
            customer_ids.append(self.add.add_customers())
        self._delete_customer.delete_customers(customer_ids)

    #打开审批
    def testOpenCustomersApprovals(self):
        _open_approvals = Approvals(self.cookie, self.csrf)
        _open_approvals.open_customer_approval()

    #关闭审批
    def testCloseCustomersApprovals(self):
        _close_approvals = Approvals(self.cookie, self.csrf)
        _close_approvals.close_customer_approval()

    #审批客户的操作
    def testApprovalCustomer(self):
        _update_customer = UpdateCustomer(self.cookie, self.csrf)
        self.testOpenCustomersApprovals()
        applying_customer_id = []
        for i in range(3):
            applying_customer_id.append(self.add.add_applying_customer())
        _update_customer.approve_customer(applying_customer_id[0])
        _update_customer.deny_customer(applying_customer_id[1])
        self.testCloseCustomersApprovals()