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

class EntitiesAdd:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testEntitiesAddByDimension(self):
        dimensions = ['created_at', 'creator_id', 'user_id']
        for dimension in dimensions:
            url = self.base_url + 'report_center/entities_add'
            params = {
                'dimension': dimension
            }
            response = self.common.get_response_json(url, params, '业务新增汇总报表： dimension是：'+ dimension)
            if not response:
                return {}
            self.filtersReport(url, params, dimension)

    def filtersByCreateAt(self, url, params, dimension):
        params['utf8'] = '✓'
        params['department_id'] = ''
        params['reator_id'] = ''
        params['start_date'] = ''
        params['end_date'] = ''

        create_at_list = ['today', 'week', 'month', 'year']
        for create_at in create_at_list:
            params['date'] = create_at
            self.common.get_response_json(url, params, '业务新增汇总报表: dimension 是：'+dimension+'按照时间维度')

    def filtersByCreatorId(self, url, params, dimension):
        params['utf8'] = '✓'
        params['department_id'] = ''
        params['reator_id'] = ''
        date_list = ['all', 'today', 'week', 'month', 'quarter', 'year', 'other']
        for date in date_list:
            if date == 'other':
                params['start_date'] = '2018-04-11'
                params['end_date'] = '2018-04-30'
            else:
                params['start_date'] = ''
                params['end_date'] = ''
            params['date'] = date
            self.common.get_response_json(url, params, '业务新增汇总报表：dimension 是：'+dimension+'按照创建时间')

    def filtersReport(self, url, params, dimension):
        if dimension == 'created_at':
            self.filtersByCreateAt(url, params, dimension)
        else:
            self.filtersByCreatorId(url, params, dimension)
        self.commonFilter.filters_by_department(url, params, '业务新增汇总报表:按照跟进部门搜索')
        self.commonFilter.filters_by_user(url, params, '业务新增汇总报表:按照跟进人用户搜索')