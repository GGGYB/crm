# -*- coding: utf-8 -*-
__author__ = 'Jun'

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

class UpdateExpenseCenters:
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
        self.expense_account_ids =[]
        self.params = ''
        self.cexpense_account_id = ''
        pass


    #开启费用报销审批
    def open_expense_account_approval(self):
        url = self.base_url + 'settings/customer_approve/update'
        params = {
            'expense_account_approve[enable_expense_account_approve]': '1'
        }
        self.common.put_response_json(url, params, '开启审批')

    # 关闭费用报销审批
    def close_expense_account_approval(self):
        url = self.base_url + 'settings/customer_approve/update'
        params = {
            'expense_account_approve[enable_expense_account_approve]': '0'
        }
        self.common.put_response_json(url, params, '关闭审批')

    # 审批报销单
    def approve_expense_accounts(self, expense_account_id):
        url = self.base_url + 'api/approvals/' + str(expense_account_id) + '/approve'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'expense_account',
            'expense_account[step]': '1',
            'expense_account[approve_description]': '审批通过',
            'expense_account[notify_user_ids][]': '',
        }
        self.common.post_response_json(url, body, '审批报销单通过')

    # 审批否决报销单
    def deny_expense_accounts(self, expense_account_id):
        url = self.base_url + 'api/approvals/' + str(expense_account_id) + '/deny'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'expense_account',
            'expense_account[approve_description]': '不予通过',
            'expense_account[step]': '1'
        }
        self.common.post_response_json(url, body, '审批否决报销单')

    # 审批报销单时编辑通知他人
    def update_notify_user(self, expense_account_id, user_id):
        url = self.base_url + 'api/approvals/' + str(expense_account_id) + '/update_notify_users'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'expense_account',
            'expense_account[notify_user_ids][]': self.user.getMyUserId(),
        }
        self.common.post_response_json(url, body, '审批通过时通知他人')