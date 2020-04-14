# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class ProductSalesStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testProductSalesStatsByDimension(self):
        dimensions = ['product', 'category', 'time']
        for dimension in dimensions:
            url = self.base_url + 'report_center/revisit_logs'
            params = {
                'dimension': dimension
            }
            response = self.common.get_response_json(url, params, '产品销售汇总报表： dimension是：'+ dimension)
            if not response:
                return {}
            self.filtersReport(url, params)

    def filtersReport(self, url, params):
        params['utf8'] = '✓'
        params['start_date'] = ''
        params['end_date'] = ''
        params['department_id'] = ''
        params['user_id'] = ''
        params['product_category_id'] = ''
        dates = ['all', 'today', 'week', 'month', 'quarter', 'year', 'other']
        for date in dates:
            if date == 'other':
                params['start_date'] = '2018-06-07'
                params['end_date'] = '2018-07-07'
            params['date'] = date
            self.common.get_response_json(url, params, '产品销售汇总报表：按照合同签约日期')
        self.commonFilter.filters_by_department(url, params, '产品销售汇总报表：按照部门')
        self.commonFilter.filters_by_user(url, params, '产品销售汇总报表：按照用户')