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

class SalesFunnel:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testSalesFunnel(self):
        url = self.base_url + 'report_center/sales_funnel'
        params = {}
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.filters_by_date(url, params)
        self.commonFilter.filters_by_department(url, params, '销售漏斗报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '销售漏斗报表:按照负责人 用户搜索')

    def filters_by_date(self, url, params):
        params = {
            'utf8': '✓'
        }

        dates = ['all', 'week', 'month', 'quarter', 'year', 'other']
        for date in dates:
            if date == 'other':
                params['start_date'] = '2018-03-09'
                params['end_date'] = '2018-04-09'
            else:
                params['start_date'] = ''
                params['end_date'] = ''
            params['date'] = date
            self.common.get_response_json(url, params, '销售漏斗报表：预计签单时间'+date)
