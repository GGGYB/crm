# -*- coding:utf-8 -*-
__author__ = "chunli"

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class GetUser:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.baseUrl = const.BASE_URL

    def getUserId(self):
        url = self.baseUrl + 'api/users'
        params = {
            'page':'',
            'perPage':''
        }
        response = self.common.get_response_json(url, params, '获取用户')
        if not response:
            return {}
        user_models = response.json()['models']
        user_ids = []
        for user in user_models:
            user_ids.append(user['id'])
        return user_ids

    def getUserIdByDepartment(self, department_id):
        url = self.baseUrl + 'api/users'
        params = {
            'page': '',
            'perPage': '',
            'department_id': department_id,
            'user_id': '',
            'username': ''
        }
        response = self.common.get_response_json(url, params, '获取用户通过部门用户id')
        if not response:
            return {}
        user_models = response.json()['models']
        user_ids = []
        if user_models != '':
            for user in user_models:
                user_ids.append(user['id'])
        return user_ids

    def getMyUserId(self):
        url = self.baseUrl + 'leads/'
        response = self.common.get_html(url, '获取用户ID')
        if not response:
            return {}
        html_str = response.text
        soup = BeautifulSoup(html_str, "html.parser")
        result_list = re.findall(r'''user_(.*?)_temp_access_token''', str(soup))
        return result_list[0]
