# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class GetReceivedPayments:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.customers_id = []
        self.params = ''
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        pass

    # # 获得回款计划、回款记录、开票记录的查询
    # #scope:'received_payment_plans';  'received_payments';  'invoiced_payments'
    # def get_received_payment_centers_scope(self):
    #     url = self.base_url + '/received_payment_center/'
    #     params = {
    #         'scope':'received_payments',
    #         'section_only':'true'
    #     }
    #     response = self.common.get_response_json(url, params, '获取线索页面的scope')
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     scopes = re.findall(r"received_payment_center/received_payments\?scope=(.*?)\">",str(soup))
    #     return scopes

    #获得回款计划的查询
    def get_received_payment_plans_scope(self):
        url = self.base_url + '/received_payment_center/received_payment_plans?scope=received_payment_plans'
        params = {
            'scope':'received_payment_plans',
            'section_only':'true',
        }
        response = self.common.get_response_json(url, params, '获取回款计划页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"/received_payment_center/received_payment_plans\?scope=(.*?)\">",str(soup))
        return scopes

    # 获得回款记录的查询
    def get_received_payment_scope(self):
        url = self.base_url + '/received_payment_center/received_payments?scope=received_payments'
        params = {
            'scope':'received_payments',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取回款记录页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"/received_payment_center/received_payments\?scope=(.*?)\">",str(soup))
        return scopes

    # 获得开票记录的查询
    def get_invoiced_payments_scope(self):
        url = self.base_url + '/received_payment_center/invoiced_payments?scope=invoiced_payments'
        params = {
            'scope':'invoiced_payments',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取开票记录页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"/received_payment_center/invoiced_payments\?scope=(.*?)\">",str(soup))
        return scopes
