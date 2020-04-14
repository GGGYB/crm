# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class DeleteContract:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.contracts_id =[]
        pass

    #删除单个合同
    def delete_contract(self, contract_id):
        url = self.base_url + 'contracts/'+str(contract_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前合同')
        return response
    #批量删除合同已不可用
    def delete_contracts(self, contract_ids):
        url = self.base_url + 'contracts/bulk_delete'
        print (url)
        body = [("utf8", "✓"), ("authenticity_token", self.csrf), ("contract_ids[]", contract_ids[0]), ("contract_ids[]", contract_ids[1])]
        print(body)
        response = self.common.delete_response_json(url, body, '批量删除合同')
        if not response:
            return {}
        self.response = response
        # return self.response.json()

    # 批量删除合同已不可用
    def delete_contracts_all(self, contract_ids):
        url = self.base_url + 'contracts/bulk_delete'
        for i in range(len(contract_ids)):
            contract_info = ("contract_ids[]", contract_ids[i])
        body = [("utf8", "✓"), ("authenticity_token", self.csrf)]
        for i in range(len(contract_ids)):
            contract_info = ("contract_ids[]", contract_ids[i])
            body.append(contract_info)
        print (body)
        response = self.common.delete_response_json(url, body, '批量删除合同')
        if not response:
            return {}
        self.response = response
        # return self.response.json()

    #获取当前页的contract id
    def get_contract_ids(self):
        url = self.base_url + 'contracts?scope=all_own&section_only=true'
        body = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '删除合同时获取所有合同')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S,'html.parser')
        contract_id_list = re.findall(r"data-id=\"(.*?)\">", str(soup))
        page = re.findall(r"data-total-pages=\"(.*?)\">", str(soup))
        return page,contract_id_list
