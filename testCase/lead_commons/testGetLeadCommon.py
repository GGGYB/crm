# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
import importlib.util
from decimal import Decimal as D
from commons import common
from commons.const import const


class GetLeadCommonId:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def  get_lead_common(self):
        self.get_lead_common_scope()

    # 获取线索池ID
    def get_lead_common_id(self):
        url = self.base_url + 'settings/lead_commons'
        body = {}
        self.response = self.common.get_response_json(url, body, '获取线索池ID')
        html_str = self.response.content
        soup = BeautifulSoup(html_str, "html.parser")
        lead_commons= soup.findAll(attrs={'class': 'dropdown-menu'})
        lead_common_id = re.findall(r"\d+\.?\d*", str(lead_commons))
        return lead_common_id[0]

     # 获取到线索池的scope
    def get_lead_common_scope(self):
        lead_common_id = self.get_lead_common_id()
        url = self.base_url + 'lead_commons/'
        params = {
            'common_id': lead_common_id,
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取线索池页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = soup.findAll(attrs={'class': 'nav-link'})
        scope = re.findall(r"/lead_commons\?common_id=(.*?)\">",str(scopes))
        return scope[0]
