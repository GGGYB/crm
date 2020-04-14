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
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departments

class CommonFilterReport:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.user = users.GetUser(cookie,csrf)
        self.department = departments.GetDepartment(cookie, csrf)
        pass

    def filters_by_create_date(self, url, params, report_name):
        params['real_date'] = 'all'
        for create_time in const.REPORT_TIME:
            if create_time == 'other':
                params['created_start_date'] = '2018-04-13'
                params['created_end_date'] = '2018-04-25'
            else:
                params['created_start_date'] = ''
                params['created_end_date'] = ''
            params['created_date'] = create_time
            self.common.get_response_json(url, params, report_name + ' 按照写跟进时间搜索：'+create_time)

    def filters_by_real_create_date(self, url, params,report_name):
        params['create_time'] = 'all'
        for real_date in const.REPORT_TIME:
            if real_date == 'other':
                params['real_start_date'] = '2018-04-13'
                params['real_end_date'] = '2018-04-25'
            else:
                params['real_start_date'] = ''
                params['real_end_date'] = ''
            params['real_date'] = real_date
            self.common.get_response_json(url, params, report_name + '按照实际跟进时间搜索：'+real_date)

    def filters_by_department(self, url, params, report_name):
        department_ids = self.department.getDepartmentId()
        for department_id in department_ids:
            params['department_id'] = department_id
            self.common.get_response_json(url, params, report_name +'按照跟进部门搜索')

    def filters_by_user(self, url, params, report_name):
        user_ids = self.user.getUserId()
        for user_id in user_ids:
            params['user_id'] = user_id
            self.common.get_response_json(url, params, report_name + '按照跟进人用户搜索')

    def filters_by_user_with_department(self, url, params, report_name):
        department_ids = self.department.getDepartmentId()
        for department_id in department_ids:
            user_id = self.user.getUserIdByDepartment(department_id)
            if user_id != '':
                for id in user_id:
                    params['user_id'] = id
                    self.common.get_response_json(url, params, report_name + '按照带部门的用户搜索')