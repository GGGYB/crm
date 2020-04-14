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

class Approvals:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def open_contract_approval(self):
        url = self.base_url + 'settings/contract_approve/update'
        params = {
            'contract_approve[enable_contract_approve]': '1'
        }
        self.common.put_response_json(url, params, '开启审批')


    def close_contract_approval(self):
        url = self.base_url + 'settings/contract_approve/update'
        params = {
            'contract_approve[enable_contract_approve]': '0'
        }
        self.common.put_response_json(url, params, '关闭审批')

    # 合同审批
    def verify_contracts(self, contracts_id):
        url = self.base_url + 'api/approvals/' + str(contracts_id) + '/approve'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            '_method': 'put',
            'key': 'contract',
            'contract[step]': '1',
            'contract[approve_description]': '123123',
            'contract[notify_user_ids][]': ''
        }
        success = self.common.post_response_json(url, body, 'verify contracts')
        if not success:
            return {}
        # return self.response.json()

    # 合同审批否决
    def deny_contracts(self, contracts_id):
        url = self.base_url + 'api/approvals/' + str(contracts_id) + '/deny'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            '_method': 'put',
            'key': 'contract',
            'contract[step]': '1',
            'contract[approve_description]': '123123',
            'contract[notify_user_ids][]': ''
        }
        success = self.common.post_response_json(url, body, 'deny contracts')
        if not success:
            return {}
        # return self.response.json()

    #合同撤销
    def cancel_contracts(self,contracts_id):
        url = self.base_url + 'api/approvals/'+ str(contracts_id) + '/revert?key=contract'
        body = {
            'utf8':'✓',
            'authenticity_token': self.csrf,
            '_method':'put',
            'key':'contract',
            'contract[approve_description]':'123123',
            }
        success = self.common.post_response_json(url, body, 'deny contracts')
        if not success:
            return {}
        # return self.response.json()