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

class RevisitLogs:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testRevistLogReportByDimension(self):
        dimensions = ['revisit_loggable', 'revisit_category']
        for dimension in dimensions:
            url = self.base_url + 'report_center/revisit_logs'
            params = {
                'dimension': dimension
            }
            response = self.common.get_response_json(url, params, '跟进对象的跟进记录报表： dimension是：'+ dimension)
            if not response:
                return {}
            self.filtersReport(url, params)

    def filtersReport(self, url, params):
        params['utf8'] = '✓'
        params['created_start_date'] = ''
        params['created_end_date'] = ''
        params['real_start_date'] = ''
        params['real_end_date'] = ''
        params['department_id'] = ''
        params['user_id'] = ''
        self.commonFilter.filters_by_create_date(url, params, '跟进记录报表')
        self.commonFilter.filters_by_real_create_date(url, params, '跟进记录报表')
        self.commonFilter.filters_by_department(url, params, '跟进记录报表')
        self.commonFilter.filters_by_user(url, params, '跟进记录报表')