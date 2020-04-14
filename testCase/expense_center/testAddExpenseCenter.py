# -*- coding: utf-8 -*-
__author__ = 'Jun'

#引入库
from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
import importlib.util
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.customers.testAddCustomer import AddCustomer
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class AddExpenseCenters:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.user = users.GetUser(cookie, csrf)
        self.expense_centers_id =[]
        self.params = ''
        self.expense_center_id = ''
        pass

    #新增费用
    def add_expenses(self):
        url = self.base_url +'api/expenses'
        body ={
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'expense[id]':'',
            'expense[related_item_type]':'',
            'last_expense_id':'',
            'expense[sn]': '10000',
            'expense[category]': '91962',
            'expense[description]': '10000',
            'expense[amount]': '5000',
            'expense[incurred_at]': '2018-08-28',
            'expense[customer_id]': self.testAddCustomer.add_customers(),
            'expense[contacts_expenses]':'',
            'expense[related_item_id]':'',
            'expense[revisit_log_id]':'',
            'expense[checkin_id]':'',
            'expense[user_id]': self.user.getMyUserId(),
        }
        response = self.common.post_response_json(url, body, '新增费用 api是'+url)
        if not response:
            return {}
        self.response = response
        print(response.json())
        expense_id = self.response.json()['data']['id']
        return expense_id

    #新增报销单(未开启审批 )
    def add_expense_accounts(self):
        url = self.base_url +'api/expense_accounts'
        body ={
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'expense_account[id]':'',
            'expense_account[approve_status]': 'approved',
            'expense_account[user_id]': self.user.getMyUserId(),
            'expense_account[department_id]': self.DepartmentId.getDepartmentId(),
            'expense_account[note]':'备注123',
            'expense_ids':self.add_expenses,
        }
        response = self.common.post_response_json(url, body, '新增费用 api是'+url)
        if not response:
            return {}
        self.response = response
        expense_account_id = self.response.json()['data']['id']
        return expense_account_id

    #开启审批新增报销单
    def add_expense_accounts_applying(self):
        url = self.base_url +'api/expense_accounts'
        body ={
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'expense_account[id]':'',
            'expense_account[approve_status]': 'applying',
            'expense_account[user_id]': self.user.getMyUserId(),
            'expense_account[department_id]': self.DepartmentId.getDepartmentId(),
            'expense_account[note]':'备注123',
            'expense_ids':self.add_expenses,
        }
        response = self.common.post_response_json(url, body, '新增费用 api是'+url)
        if not response:
            return {}
        self.response = response
        expense_account_id = self.response.json()['data']['id']
        return expense_account_id


