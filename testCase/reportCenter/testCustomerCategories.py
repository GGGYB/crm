# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

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
from .testCommonFilterReport import CommonFilterReport

class CustomerCategoried:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #客户类型统计报表
    def testCustomerCategoried(self):
        url = self.base_url + 'report_center/customer_categories'
        params = {}
        response = self.common.get_response_json(url, params, '客户类型统计报表')
        if not response:
            return {}
        else:
            content = response.content
            print(content)
            soup = BeautifulSoup(content, "html.parser",from_encoding="iso-8859-1")
            statusNode = soup.find_all('a',class_='link_status ')
            print(statusNode)
            # a = re.findall(r"value=\"(.*?)\"",str(soup))
            # print (a)
            # self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.commonFilter.filters_by_department(url, params, '客户类型统计报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '客户类型统计报表:按照负责人 用户搜索')


