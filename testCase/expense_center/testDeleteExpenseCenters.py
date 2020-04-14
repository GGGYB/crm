# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import re
from commons import common
from commons.const import const
from testCase.customers.testAddCustomer import AddCustomer
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class DeleteExpenseCenters:
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
        self.expense_ids =[]
        self.params = ''
        self.expense_id = ''
        self.expense_account = ''
        self.expense_accounts = ''
        pass

    #删除单个费用
    def delete_expense(self, expense_id):
        url = self.base_url + 'expense_centers/'+str(expense_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前费用')
        return response

    #批量删除费用
    def delete_expenses(self, expense_ids):
        url = self.base_url + 'expenses/bulk_delete'
        body = [("utf8", "✓"), ("authenticity_token", self.csrf,), ("expense_ids[]", expense_ids[0]), ("expense_ids[]", expense_ids[1])]
        response = self.common.delete_response_json(url, body, '批量删除费用')
        if not response:
            return {}
        self.response = response

    #获取当前页的费用id:(expense_id)
    def get_expense_ids(self):
        url = self.base_url + 'expense_center/expenses?scope=all_own&section_only=true'
        body = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '获取所有费用')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S)
        checked_expense = soup.find(attrs={'data-entity-table-name':'expense'})
        if checked_expense:
            a = str(checked_expense)
            expense_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return expense_id_list

    #删除单个报销单
    def delete_expense_account(self, expense_account_id):
        url = self.base_url + 'expense_centers/'+str(expense_account_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前报销单')
        return response

    #批量删除报销单
    def delete_expense_accounts(self, expense_account_ids):
        url = self.base_url + 'expense_accounts/bulk_delete'
        body = [("utf8", "✓"), ("authenticity_token", self.csrf,), ("expense_ids[]", expense_account_ids[0]), ("expense_account_ids[]", expense_account_ids[1])]
        response = self.common.delete_response_json(url, body, '批量删除报销单')
        if not response:
            return {}
        self.response = response

    #获取当前页的报销单id(expense_account_id)
    def get_expense_account_ids(self):
        url = self.base_url + 'expense_center/expense_accounts?scope=all_own&section_only=true'
        body = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '获取所有报销单')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S)
        checked_expense_account = soup.find(attrs={'data-entity-table-name':'expense_account'})
        if checked_expense_account:
            a = str(checked_expense_account)
            expense_account_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return expense_account_id_list
