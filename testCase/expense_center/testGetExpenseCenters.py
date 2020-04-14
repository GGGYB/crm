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

class GetExpenseCenters:
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
        self.contracts_id =[]
        self.params = ''
        self.contract_id = ''
        pass


    def get_expense_center(self):
        self.export_selected_expense_accounts()
        self.export_all_expense_accounts()
        self.get_expense_accounts()
        self.get_expenses()
    """
    ******************
         报销单
    *****************
    """
    #获得所有报销单、我的报销单
    def get_all_expense_accounts_scope(self):
        url = self.base_url + 'expense_center/expense_accounts'
        params = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取线索页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"\?scope=(.*?)\">",str(soup))
        return scopes

    # 获取当前页的报销单id(expense_account_id)
    def expense_account_ids(self):
        url = self.base_url + 'expense_center/expense_accounts'
        body = {
            'order': 'asc',
            'scope': 'all_own',
            'sort': 'leads.updated_at desc',
            'per_page': 10,
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的报销单id')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, "html.parser")
        checked_expense_account = soup.find(attrs={'data-entity-table-name': 'expense_accounts'})
        if checked_expense_account:
            a = str(checked_expense_account)
            expense_account_list = re.findall(r"data-id=\"(.*?)\">", a)
            return expense_account_list

    # 获取单个报销单详情
    def get_expense_accounts(self, expense_account_id):
        url = self.base_url + 'expense_accounts/' + str(expense_account_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前报销单详情')
        if response != False:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

    # 导出所选报销单
    def export_selected_expense_accounts(self, scope):
        expense_account_ids = self.expense_account_ids()
        url = self.base_url + 'expense_center/expense_accounts?export_page=1&amp;format_type=calculate_export_pages&amp;per_page=10&amp;scope=' + scope + '&amp;sort=expense_accounts.updated_at+desc&amp;type=advance&selected_ids%5B%5D=' + \
              expense_account_ids[0] + '&selected_ids%5B%5D=' + expense_account_ids[1] + '&format=js'
        self.common.get_response_json(url, 'export_selected_expense_accounts')
        url = self.base_url + 'expense_center/expense_accounts.js?export_page=1&format_type=xlsx&per_page=10&scope=' + scope + '&selected_ids%5B%5D=' + \
              expense_account_ids[0] + '&selected_ids%5B%5D=' + expense_account_ids[1] + '&sort=leads.updated_at+desc&type=advance'
        self.common.get_response_jsonn(url, 'excute download export selected file')

    # 导出全部报销单
    def export_all_expense_accounts(self, scope):
        url = self.base_url + 'expense_center/expense_accounts?format_type=calculate_export_pages&per_page=10&scope=' + scope + '&sort=expense_accounts.updated_at+desc&type=advance'
        self.common.get_response_json(url, 'export_all_expense_accounts')
        # 点击下载文档
        url = self.base_url + 'expense_center/expense_accounts?export_page=1&format_type=xlsx&per_page=10&scope=' + scope + '&sort=expense_accounts.updated_at+desc&type=advance'
        self.common.get_response_json(url, 'excute download export all expense_accounts file')

    """
    ******************
          费用
    *****************
    """
    #获得所有费用、我的费用
    def get_all_expense_scope(self):
        url = self.base_url + 'expense_center/expenses'
        params = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取线索页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"\?scope=(.*?)\">",str(soup))
        return scopes

    # 获取当前页的费用id(expense_account_id)
    def expense_ids(self):
        url = self.base_url + 'expense_center/expenses'
        body = {
            'order': 'asc',
            'scope': 'all_own',
            'sort': 'leads.updated_at desc',
            'per_page': 10,
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的报销单id')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, "html.parser")
        checked_expense_account = soup.find(attrs={'data-entity-table-name': 'expenses'})
        if checked_expense_account:
            a = str(checked_expense_account)
            expense_account_list = re.findall(r"data-id=\"(.*?)\">", a)
            return expense_account_list

    # 获取单个费用详情
    def get_expenses(self, expense_id):
        url = self.base_url + 'expenses/' + str(expense_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前费用详情')
        if response != False:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

    # 导出所选费用
    def export_selected_expenses(self, scope):
        expense_ids = self.expense_ids()
        url = self.base_url + 'expense_center/expenses?export_page=1&amp;format_type=calculate_export_pages&amp;per_page=10&amp;scope=' + scope + '&amp;sort=expenses.updated_at+desc&amp;type=advance&selected_ids%5B%5D=' + \
              expense_ids[0] + '&selected_ids%5B%5D=' + expense_ids[1] + '&format=js'
        self.common.get_response_jsonn(url, 'export_selected_expenses')
        url = self.base_url + 'expense_center/expenses.js?export_page=1&format_type=xlsx&per_page=10&scope=' + scope + '&selected_ids%5B%5D=' + \
              expense_ids[0] + '&selected_ids%5B%5D=' + expense_ids[1] + '&sort=expenses.updated_at+desc&type=advance'
        self.common.get_response_json(url, 'excute download export selected file')
    # 导出全部费用
    def export_all_expenses(self, scope):
        url = self.base_url + 'expense_center/expenses?format_type=calculate_export_pages&per_page=10&scope=' + scope + '&sort=expenses.updated_at+desc&type=advance'
        self.common.get_response_json(url, 'export_all_expense_accounts')
        # 点击下载文档
        url = self.base_url + 'expense_center/expense_accounts?export_page=1&format_type=xlsx&per_page=10&scope=' + scope + '&sort=expenses.updated_at+desc&type=advance'
        self.common.get_response_json(url, 'excute download export all expenses file')

