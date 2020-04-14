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

class Approvals:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def open_customer_approval(self):
        url = self.base_url + 'settings/customer_approve/update'
        params = {
            'customer_approve[enable_customer_approve]': '1'
        }
        self.common.put_response_json(url, params, '开启审批')

    def close_customer_approval(self):
        url = self.base_url + 'settings/customer_approve/update'
        params = {
            'customer_approve[enable_customer_approve]': '0'
        }
        self.common.put_response_json(url, params, '关闭审批')