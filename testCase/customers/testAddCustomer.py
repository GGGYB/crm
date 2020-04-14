# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.departments.testGetDepartment import GetDepartment
from testCase.users import testGetUser as users

class AddCustomer:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.testGetDepartment = GetDepartment(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.response = ''
        self.user_id = ''
        self.customers_id =[]
        self.params = ''
        pass

    #新增客户
    def add_customers(self):
        url = self.base_url + 'api/customers'
        body = {
            'utf8':'✓',
            'authenticity_token': self.csrf,
            'refer_call_record_id':'',
            'customer[id]':'',
            'customer[name]':'customers%s' %self.common.get_today_str_yymmddhhmm(),
            'customer[category]':'3611786',
            'customer[company_name]': '公司名称%s' %self.common.get_random_int(99999999),
            'customer[address_attributes][tel]':'199%s' %self.common.get_random_int(99999999),
            'customer[address_attributes][email]':'test%s@test.com' %self.common.get_random_int(9999999),
            'customer[address_attributes][fax]':self.common.get_random_int(99999999),
            'customer[address_attributes][url]':'https://www.test%s.com' %self.common.get_random_int(9999999),
            'china_tag_id':'4',
            'customer[address_attributes][country_id]':'4',
            'customer[address_attributes][province_id]':'2',
            'customer[address_attributes][city_id]':'2',
            'customer[address_attributes][district_id]':'21',
            'customer[address_attributes][detail_address]':'浦东西区%s号'%self.common.get_random_int(99999),
            'customer[address_attributes][zip]':'201203',
            'customer[status]':'',
            'customer[source]':'',
            'customer[industry]':'',
            'customer[staff_size]':'',
            'customer[revisit_remind_at]':'',
            'customer[note]':'',
            'customer[user_id]':self.user.getUserId(),
            'customer[want_department_id]':self.testGetDepartment.getDepartmentId()
        }
        response = self.common.post_response_json(url, body, '新增客户 api是'+url)
        if not response:
            return {}
        self.response = response
        customer_id = self.response.json()['data']['id']
        return customer_id

    def add_applying_customer(self):
        url = self.base_url + 'api/customers'
        body = {
            'utf8':'✓',
            'authenticity_token': self.csrf,
            'refer_call_record_id':'',
            'customer[id]':'',
            'customer[approve_status]':'applying',
            'customer[name]':'customers%s' %self.common.get_today_str_yymmddhhmm(),
            'customer[category]':'3611786',
            'customer[address_attributes][tel]':'132%s' %self.common.get_random_int(99999999),
            'customer[address_attributes][email]':'%s8@qq.com' %self.common.get_random_int(9999999),
            'customer[address_attributes][fax]':self.common.get_random_int(99999999),
            'customer[address_attributes][url]':'http://www.baidu.com',
            'china_tag_id':'4',
            'customer[address_attributes][country_id]':'4',
            'customer[address_attributes][province_id]':'2',
            'customer[address_attributes][city_id]':'2',
            'customer[address_attributes][district_id]':'21',
            'customer[address_attributes][detail_address]':'浦东西区%s号'%self.common.get_random_int(99999),
            'customer[address_attributes][zip]':'201203',
            'customer[status]':'',
            'customer[source]':'',
            'customer[industry]':'',
            'customer[staff_size]':'',
            'customer[revisit_remind_at]':'',
            'customer[note]':'',
            'customer[user_id]':'2223379',
            'customer[want_department_id]':'190227'
        }
        response = self.common.post_response_json(url, body, '开启审批新增客户 api是'+url)
        if not response:
            return {}
        self.response = response
        customer_id = self.response.json()['data']['id']
        return customer_id