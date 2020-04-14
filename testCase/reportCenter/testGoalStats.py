# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport

class GoalStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #业绩目标完成度报表
    def testGoalStats(self):
        years = ['2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            goalTypeValues = self.testGetSalesGoalByYear(year)
            for goalTypeValue in goalTypeValues:
                self.testGoalStatsByGoalType(goalTypeValue)

    def testGoalStatsByGoalType(self, goal_type_value):
        url = self.base_url + 'report_center/goal_stats'
        params = {
            'utf8': '✓',
            'due_at_year': '2016',
            'product_id': '',
            'product_category_id':'',
            'goal_type': goal_type_value,
            'department_id': '',
            'user_id': '',
        }
        self.filtersReport(url, params)

    def testGetSalesGoalByYear(self, year):
        url = self.base_url + 'api/sales_goal_yearlies/fetch_goal_types_by_year'
        params = {
            'due_at_year': year
        }
        response = self.common.get_response_json(url, params, '获取当前年份的业绩类型， 年份是：'+ year)
        list = response.json()['data']
        goal_type_value = []
        for goal_type in list:
            goal_type_value.append(goal_type[1])
        return goal_type_value

    def filtersReport(self, url, params):
        self.commonFilter.filters_by_department(url, params, '业绩目标完成度报表:按照所属部门搜索')
        self.commonFilter.filters_by_user(url, params, '业绩目标完成度报表:按照负责人 用户搜索')
