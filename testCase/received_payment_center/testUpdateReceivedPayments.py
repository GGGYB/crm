# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid


class UpdateReceivedPayments:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.customers_id = []
        self.params = ''
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        pass


    # #回款计划设置为已完成
    #  def done_received_payment_plans(self):
    #      url = self.base_url + 'api/received_payment_plans/61614/done'
    #配置回款计划(批量生成)

