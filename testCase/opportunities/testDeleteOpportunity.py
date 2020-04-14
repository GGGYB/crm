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

class DeleteOpportunities:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.opportunities_id =[]
        pass

    #删除单个商机
    def delete_opportunitie(self, opportunitie_id):
        url = self.base_url + 'opportunities/'+str(opportunitie_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前商机')
        return response
    #批量删除商机
    def delete_opportunities(self, opportunitie_ids):
        url = self.base_url + 'opportunities/bulk_delete'
        body = [("utf8", "✓"), ("authenticity_token", self.csrf,), ("opportunitie_ids[]", opportunitie_ids[0]), ("opportunitie_ids[]", opportunitie_ids[1])]
        response = self.common.delete_response_json(url, body, '批量删除商机')
        if not response:
            return {}
        self.response = response
        # return self.response.json()

    #获取当前页的opportunitie id
    def get_opportunitie_ids(self):
        url = self.base_url + 'opportunities?scope=all_own&section_only=true'
        body = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '删除商机时获取所有商机')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, 'html.parser')
        contract_id_list = re.findall(r"data-id=\"(.*?)\">", str(soup))
        page = re.findall(r"data-total-pages=\"(.*?)\">", str(soup))
        return page, contract_id_list

        # if not response:
        #     return {}
        # self.response = response
        # S = self.response.content
        # soup = BeautifulSoup(S, 'html.parser')
        # contract_id_list = re.findall(r"data-id=\"(.*?)\">", str(soup))
        # page = re.findall(r"data-total-pages=\"(.*?)\">", str(soup))
        # return page, contract_id_list
