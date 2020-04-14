# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class DeleteCustomer:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.customers_id =[]
        pass

    #删除单个客户
    def delete_customer(self, customer_id):
        url = self.base_url + 'customers/'+str(customer_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前客户')
        return response
    #批量删除客户
    def delete_customers(self, customer_ids):
        url = self.base_url + 'customers/bulk_delete'
        body = [("utf8", "✓"), ("authenticity_token", self.csrf,), ("customer_ids[]", customer_ids[0]), ("customer_ids[]", customer_ids[1])]
        response = self.common.delete_response_json(url, body, '批量删除客户')
        if not response:
            return {}
        # self.response = response
        # return self.response.json()
    #获取当前页的Customer id
    def get_customer_ids(self):
        url = self.base_url + 'customers'
        body = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '删除客户时获取所有客户')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S)
        checked_customer = soup.find(attrs={'data-entity-table-name':'Customer'})
        if checked_customer:
            a = str(checked_customer)
            customer_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return customer_id_list