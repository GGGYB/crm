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

class LeadTransRate:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #线索转化率报表
    def testLeadTransRate(self):
        url = self.base_url + 'report_center/lead_trans_rate'
        params = {
            'utf8': '✓',
            'year': '2016',
            'department_id': '',
            'user_id': '',
        }
        dimensions = ['trans_rate', 'trans_interval']
        for dimension in dimensions:
            params['dimension'] = dimension
            self.filtersReport(url, params, dimension)

    def filtersReport(self, url, params, dimension):
        self.filter_by_year(url, params)
        self.commonFilter.filters_by_department(url, params, '赢单商机汇总报表: dimension是：'+dimension+'按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '赢单商机汇总报表 dimension是：'+dimension+'按照负责人 用户搜索')

    def filter_by_year(self,url, params):
        years = ['2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            params['year'] = year
            self.common.get_response_json(url, params, '赢单商机汇总报表: 时间是：'+ year)
