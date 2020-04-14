# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid
from testCase.contracts.testAddContract import AddContract
from .testAddReceivedPayments import AddReceivedPayment



class DeleteReceivedPayments:
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
        self.testAddContract = AddContract(cookie, csrf)
        self.testAddReceivedPayments = AddReceivedPayment(cookie, csrf)
        self.received_payment_ids = []
        self.received_payment_id = ''
        self.received_payment_plan_ids =[]
        self.received_payment_plan_id = ''
        pass


    #删除回款记录
    def delete_received_payment(self,contract_id,received_payments_id):
        url = self.base_url + 'contracts'+str(contract_id)+ 'invoiced_payments/'+str(received_payments_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前回款记录')
        return response

    #删除开票记录
    def delete_invoiced_payments(self,contract_id,invoiced_payments_id):
        url = self.base_url + 'contracts'+str(contract_id)+'invoiced_payments/'+str(invoiced_payments_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前开票记录')
        return response

    #批量删除回款计划
    def delete_received_payment_plans(self,scope,received_payment_plan_ids):
        url = self.base_url + 'received_payments/bulk_delete'
        body = {
            'authenticity_token':self.csrf,
            'received_payment_plan_ids[]': received_payment_plan_ids[0],
            'received_payment_plan_ids[]': received_payment_plan_ids[1],
        }
        response = self.common.delete_response_json(url, body, '批量删除回款计划')
        if not response:
            return {}

    #批量删除回款记录
    def delete_received_payments(self,scope,received_payment_ids):
        url = self.base_url + 'received_payments/bulk_delete'
        body = {
            'authenticity_token':self.csrf,
            'received_payment_ids[]': received_payment_ids[0],
            'received_payment_ids[]': received_payment_ids[1],
        }
        response = self.common.delete_response_json(url, body, '批量删除回款计划')
        if not response:
            return {}



