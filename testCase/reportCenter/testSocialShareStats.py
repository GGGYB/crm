# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class SocialShareStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    def testSocialShareStats(self):
        url = self.base_url + 'sms_marketing/report_center/social_share_stats'
        params = {}
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.filters_by_date(url, params)
        self.commonFilter.filters_by_department(url, params, '短信转化率报表:按照发信部门')
        self.commonFilter.filters_by_user_with_department(url, params, '短信转化率报表:按照发信人')

    def filters_by_date(self, url, params):
        params = {
            'utf8': '✓'
        }

        dates = ['all', 'today', 'this_week', 'this_month', 'this_quarter', 'this_year', 'visit_time']
        for date in dates:
            if date == 'visit_time':
                params['start_date'] = '2018-03-09'
                params['end_date'] = '2018-04-09'
                params['date'] = 'other'
            else:
                params['start_date'] = ''
                params['end_date'] = ''
                params['date'] = date
            params['department_id'] = ''
            params['user_id'] = ''
            self.common.get_response_json(url, params, '分析类：短信转化率报表'+date)
