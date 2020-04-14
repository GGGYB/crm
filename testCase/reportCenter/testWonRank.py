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

class WonRank:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #销售额排名报表
    def testWonRank(self):
        url = self.base_url + 'report_center/won_rank'
        params = {
            'utf8': '✓',
            'from_y_m': '2018-04',
            'to_y_m':'2018-04',
            'department_id': ''
        }
        dimensions = ['contract', 'opportunity']
        for dimension in dimensions:
            params['dimension'] = dimension
            self.commonFilter.filters_by_department(url, params, '销售额排名报表:按照所属部门搜索')