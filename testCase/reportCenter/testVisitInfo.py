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

class VisitInfo:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #拜访签到报表
    def testVisitInfo(self):
        url = self.base_url + 'report_center/visit_infos'
        params = {
            'utf8': '✓',
            'start_date': '',
            'end_date':'',
            'department_id': '',
            'user_id': '',
        }
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.filter_by_year(url, params)
        self.commonFilter.filters_by_department(url, params, '拜访签到报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '拜访签到报表:按照签到人 用户搜索')

    def filter_by_year(self,url, params):
        date_list = ['all', 'today', 'week', 'month', 'quarter', 'year','other']
        for date in date_list:
            if date == 'other':
                params['start_date'] = '2018-04-11'
                params['end_date'] = '2018-04-17'
            else:
                params['start_date'] = ''
                params['end_date'] = ''
            params['date'] = date
            self.common.get_response_json(url, params, '拜访签到报表: 签到时间是：'+ date)
