# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testCommonFilterReport import CommonFilterReport
from testCase.departments import testGetDepartment as departments

class CustomerRank:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        self.departments = departments.GetDepartment(cookie, csrf)
        pass

    def testCustomerRank(self):
        department_ids = self.departments.getDepartmentId()
        persps = ['user', 'department']
        for id in department_ids:
            for persp in persps:
                url = self.base_url + 'report_center/customers'
                params = {
                    'utf8': '✓',
                    'department_id': id,
                    'persp': 'user',
                    'from': '2018-06-01',
                    'to': '2018-06-30',
                    'commit': '查询',
                }
                response = self.common.get_response_json(url, params, '客户数量排名报表： 视角是：'+ persp)
                if not response:
                    return {}