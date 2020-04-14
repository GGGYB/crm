# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class GoalRank:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #业绩目标完成度排名报表
    def testGoalRank(self):
        url = self.base_url + ''
        params = {
            'utf8': '✓',
            'due_at_year': '2017',
            'from_y_m': '2017-01',
            'to_y_m': '2017-12',
            'product_id': '',
            'product_category_id': '',
            'goal_type': '',
            'department_id': '',
            'user_id': '',
        }
        self.common.get_response_json(url, params, '业绩目标完成度排名报表：')
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.commonFilter.filters_by_department(url, params, '业绩目标完成度报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '业绩目标完成度报表:按照负责人 用户搜索')
