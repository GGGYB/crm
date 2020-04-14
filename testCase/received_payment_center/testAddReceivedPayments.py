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
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid
from testCase.customers.testAddCustomer import AddCustomer
from testCase.contracts.testAddContract import AddContract


class AddReceivedPayment:
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
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.testAddContract = AddContract(cookie, csrf)
        self.customer_id = ''
        self.contract_id = ''
        pass



    # 新增回款计划
    def add_received_payment_plans(self):
        url = self.base_url +'api/received_payments'
        body = {
            'utf8': ' ✓',
            'authenticity_token': self.csrf,
            'plans[0][customer_id]': self.testAddCustomer.add_customers(),
            'plans[0][contract_id]': self.testAddContract.add_contracts(),
            'plans[0][receive_stage]': '1',
            'plans[0][receive_date]': '2018-08-01',
            'plans[0][amount]': '4500',
            'plans[0][note]':''

        }
        response = self.common.post_response_json(url, body, '新增回款计划 api是' + url)
        if not response:
            return {}
        self.response = response
        received_payments_id = self.response.json()['data']['id']
        return received_payments_id

    #获取回款计划id
    def received_payment_plan_id_get(self, contract_id,):
        url = self.base_url +'contracts/%s?tab=tab_received_payments' %contract_id
        body ={}
        response = self.common.get_response_json(url, body, '获取回款计划id api是' + url)
        self.response = response
        S = self.response.text
        soup = BeautifulSoup(S, 'html.parser')
        received_payment_plan_id = re.findall(r"received_payment_plan_id: (.*?),", str(soup))
        return received_payment_plan_id

    # 获取回款计划id按照回款页面
    def received_payment_plan_id_get_page(self):
        url = self.base_url + 'received_payment_center/received_payment_plans?scope=received_payment_plans&per_page=10&type=advance&section_only=true'
        body = {}
        response = self.common.get_response_json(url, body, '获取回款计划id api是' + url)
        self.response = response
        S = self.response.text
        soup = BeautifulSoup(S, 'html.parser')
        # print (str(soup))
        received_payment_plan_id = re.findall(r"data-id=\"(.*?)\">", str(soup))
        return received_payment_plan_id

    # 新增回款记录
    def add_received_payments(self, contract_id,receive_date ='2018-06-22',amount ='2000',customer_id =''):
        url = self.base_url +'api/received_payments'
        body = {
            'utf8': ' ✓',
            'authenticity_token': self.csrf,
            'request_ticket': self.common.get_random_int(9999999999999),
            'contract_id': contract_id,
            'received_payment[receive_date]': receive_date,
            'received_payment[amount]': amount,
            'received_payment[customer_id]': customer_id,
            'received_payment[contract_id]': contract_id,
            'received_payment[received_payment_plan_id]': self.received_payment_plan_id_get_page()[0],
            'received_payment[payment_type]': '',
            'received_payment[received_types]': '',
            'received_payment[receive_user_id]': self.user.getMyUserId(),
            'received_payment[note]': '备注',
        }
        response = self.common.post_response_json(url, body, '新增回款记录 api是' + url)
        if not response:
            return {}
        self.response = response
        received_payments_id = self.response.json()['data']['id']
        return received_payments_id

    # 新增开票记录
    def add_invoiced_payments(self, contract_id):
        url = self.base_url + 'api/invoiced_payments'
        body = {
            'utf8': ' ✓',
            'authenticity_token': self.csrf,
            'invoiced_payment[amount]': '2000',
            'invoiced_payment[invoice_types]': '205671',
            'invoiced_payment[invoice_no]': '',
            'invoiced_payment[note]': '备注',
            'invoiced_payment[invoiced_date]': '2018-06-23',
            'invoiced_payment[broker_user_id]': self.user_id,
            'invoiced_payment[content]': '开票' % self.common.get_random_int(99999),
        }
        response = self.common.post_response_json(url, body, '新增开票记录 api是' + url)
        if not response:
            return {}
        self.response = response
        invoiced_payment_id = self.response.json()['data']['id']
        return invoiced_payment_id