# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class SMSReachRateStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testSMSReachRateStats(self):
        url = self.base_url + 'report_center/sales_funnel'
        params = {
            'utf8': '✓'
        }
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.filters_by_date(url, params)
        self.commonFilter.filters_by_department(url, params, '短信到达率报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '短信到达率报表:按照负责人 用户搜索')

    def filters_by_date(self, url, params):
        dates = ['2015', '2016', '2017', '2018', '2019', '2020']
        for date in dates:
            params['due_at_year'] = date
            self.common.get_response_json(url, params, '短信到达率报表：时间'+date)