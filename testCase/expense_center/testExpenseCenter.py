# -*- coding: utf-8 -*-
__author__ = 'Jun'
#引入库
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
from .testAddExpenseCenter import AddExpenseCenters
from .testGetExpenseCenters import GetExpenseCenters
from .testUpdateExpenseCenters import UpdateExpenseCenters
from .testDeleteExpenseCenters import DeleteExpenseCenters
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class ExpenseCenters:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        self.add_expense_centers = AddExpenseCenters(cookie, csrf)
        self.get_expense_centers = GetExpenseCenters(cookie, csrf)
        self.update_expense_centers = UpdateExpenseCenters(cookie, csrf)
        self.delete_expense_centers = DeleteExpenseCenters(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.expense_center_id = ''
        pass


    def testExpenseCenters(self):
        self.testAddExpenseCenter()
        scopes = self.get_expense_centers.get_all_expense_accounts_scope()
        scopes = self.get_expense_centers.get_all_expense_scope()
        self.testGetExpenseCenters(scopes)
        self.testUpdateExpenseCenters(scopes)
        self.testDeleteExpenseCenters()

    def testAddExpenseCenter(self):
        self.add_expense_centers.add_expenses()
        self.add_expense_centers.add_expense_accounts()
        self.update_expense_centers.open_expense_account_approval()
        self.applying_expense_account = self.add_expense_centers.add_expense_accounts_applying()
        self.update_expense_centers.close_expense_account_approval()

    def testGetExpenseCenters(self, scopes):
        self.update_expense_centers.close_expense_account_approval()
        self.filters.expense_center_filters_by_business('expenses', scopes)
        expense_id = self.add_expense_centers.add_expenses()
        self.get_expense_centers.get_expenses(expense_id)
        expense_account_id = self.add_expense_centers.add_expense_accounts()
        self.get_expense_centers.get_expense_accounts(expense_account_id)

    # #打开审批
    # def testOpenExpenseCentersApprovals(self):
    #     _open_approvals = Approvals(self.cookie, self.csrf)
    #     _open_approvals.open_expense_account_approval()
    #
    # #关闭审批
    # def testCloseExpenseCentersApprovals(self):
    #     _close_approvals = Approvals(self.cookie, self.csrf)
    #     _close_approvals.close_expense_account_approval()

    #编辑报销单/费用
    def testUpdateExpenseCenters(self, scopes):
        expense_account_id = self.add_expense_centers.add_expense_accounts()
        user_id = self.user.getMyUserId()
        self.update_expense_centers.open_expense_account_approval()
        self.update_expense_centers.approve_expense_accounts(expense_account_id)
        self.update_expense_centers.deny_expense_accounts(expense_account_id)
        self.update_expense_centers.update_notify_user(expense_account_id, user_id)
        self.update_expense_centers.close_expense_account_approval()


    #删除报销单/费用
    def testDeleteExpenseCenters(self):
        #删除单个报销单/费用
        customer_id = self.add_expense_centers.add_customers()
        self.delete_expense_centers.delete_customer(customer_id)
        #批量删除报销单/费用
        customer_ids = []
        for i in range(2):
            customer_ids.append(self.add_expense_centers.add_customers())
        self.delete_expense_centers.delete_customers(customer_ids)
