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

class GetCustomerCommons:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    #获得所有的我的客户，我协作的客户，我的客户来查询
    def get_all_scope(self):
        url = self.base_url + 'customer_commons'
        params = {
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取线索页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        navs = soup.find(attrs={'class':'nav-tabs'})
        customer_common_ids = re.findall(r"\/customer_commons\?common_id=(.*?)&amp;", str(navs))
        return customer_common_ids

