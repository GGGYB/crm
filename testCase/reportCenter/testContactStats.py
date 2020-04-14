# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class ContractsStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #合同汇总报表
    def testContractsStats(self):
        url = self.base_url + 'report_center/contracts_stats'
        params = {
            'utf8': '✓',
            'year': '2016',
            'category': '',
            'department_id': '',
            'user_id': '',
        }
        response = self.common.get_response_json(url, params, '获取合同汇总报表页面')
        if not response:
                return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        # self.filter_by_contract_type(soup, url, params)
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.filter_by_year(url, params)
        self.commonFilter.filters_by_department(url, params, '赢单商机汇总报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '赢单商机汇总报表:按照负责人 用户搜索')

    def filter_by_contract_type(soup, self, url, params):
        searchWrappers = soup.find(attrs={'class':'search-link'})
        types = re.findall(r"value=\"(.*?)\">",str(searchWrappers))


    def filter_by_year(self,url, params):
        years = ['2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            params['year'] = year
            self.common.get_response_json(url, params, '赢单商机汇总报表: 时间是：'+ year)