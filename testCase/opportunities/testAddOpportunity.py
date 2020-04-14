# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
import importlib.util
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.customers.testAddCustomer import AddCustomer
from testCase.departments.testGetDepartment import GetDepartment
from testCase.users import testGetUser as users


class AddOpportunities:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        # self.testCase.customers = add_customers
        # self.testAddCustomer = AddCustomer
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.testGetDepartment = GetDepartment(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.opportunities_id =[]
        self.params = ''
        self.opportunity_id = ''
        pass

    # 新增商机（关闭审批）
    def add_opportunities(self,sign_date ='2018-05-16',total_amount=500,approve_status='approved',stage ='',DepartmentId=0):
        # self.testAddCustomer.add_customers()
        # self.testGetDepartment.getDepartmentId()
        url = self.base_url + 'api/opportunities'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'refer_call_record_id': '',
            # 'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            'request_ticket': self.common.get_random_int(99999999),
            'opportunity[id]':'',
            'opportunity[approve_status]': approve_status,
            'opportunity[title]': 'opportunity%s' % self.common.get_random_int(99999999),
            # 'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            'opportunity[customer_id]':'1228332',
            'opportunity[expect_amount]': total_amount,
            'opportunity[expect_sign_date]': sign_date,
            'opportunity[stage]': stage,
            'opportunity[kind]':'',
            'opportunity[get_time]': '2018-07-03',
            'opportunity[source]': '205676',
            'opportunity[revisit_remind_at]':'2018-09-14 19:00',
            'opportunity[note]':'',
            'opportunity[user_id]':self.user.getMyUserId(),
            'opportunity[want_department_id]':self.testGetDepartment.getDepartmentId()[DepartmentId]
        }
        response = self.common.post_response_json(url, body, '新增商机 api是'+url)
        if not response:
            return {}
        self.response = response
        opportunity_id = self.response.json()['data']['id']
        return opportunity_id


    #新增待审批商机
    def add_applying_opportunities(self):
        url = self.base_url + 'api/opportunities'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            # 'request_ticket': '23ca40d3-e1ee-468b-9d25-710bb0306d30',
            'opportunity[id]':'',
            'opportunity[approve_status]': 'applying',
            'opportunity[title]': 'opportunity%s' % self.common.get_random_int(99999999),
            'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            # 'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            # 'opportunity[product_assets_attributes][][id]':'',
            # 'opportunity[product_assets_attributes][][_destroy]': 'false',
            # 'opportunity[product_assets_attributes][][product_id]': '',
            # 'opportunity[product_assets_attributes][][recommended_unit_price]': '',
            # 'opportunity[product_assets_attributes][][quantity]': '',
            # 'opportunity[product_assets_attributes][][remark]':'',
            # 'opportunity[product_assets_attributes][][product_attr_id]':'',
            'opportunity[expect_amount]': '5000',
            'opportunity[expect_sign_date]': '2018-05-16',
            'opportunity[stage]': '81797',
            'opportunity[kind]':'',
            'opportunity[get_time]': '2018-07-06',
            'opportunity[source]': '',
            'opportunity[revisit_remind_at]':'2018-09-14 19:00',
            'opportunity[note]':'',
            # 'opportunity[user_id]':self.user.getUserId()[0] ,    #,"2222396"
            'opportunity[want_department_id]': str(self.testGetDepartment.getDepartmentId()[0])  #5168
        }
        response = self.common.post_response_json(url, body, '开启审批新增商机 api是'+url)
        if not response:
            return {}
        self.response = response
        opportunity_id = self.response.json()['data']['id']
        print(opportunity_id)
        return opportunity_id

    # 撤销之后重新提交商机审批
    def re_add_applying_opportunities(self,opportunity_id):
        url = self.base_url + 'api/opportunities/' + str(opportunity_id)
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            # 'request_ticket': '23ca40d3-e1ee-468b-9d25-710bb0306d30',
            'opportunity[id]': opportunity_id,
            'opportunity[approve_status]': 'applying',
            'opportunity[title]': 'opportunity%s' % self.common.get_random_int(99999999),
            'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            # 'opportunity[customer_id]': self.testAddCustomer.add_customers(),
            # 'opportunity[product_assets_attributes][][id]':'',
            # 'opportunity[product_assets_attributes][][_destroy]': 'false',
            # 'opportunity[product_assets_attributes][][product_id]': '',
            # 'opportunity[product_assets_attributes][][recommended_unit_price]': '',
            # 'opportunity[product_assets_attributes][][quantity]': '',
            # 'opportunity[product_assets_attributes][][remark]':'',
            # 'opportunity[product_assets_attributes][][product_attr_id]':'',
            'opportunity[expect_amount]': '5000',
            'opportunity[expect_sign_date]': '2018-05-16',
            'opportunity[stage]': '81797',
            'opportunity[kind]': '',
            'opportunity[get_time]': '2018-07-06',
            'opportunity[source]': '',
            'opportunity[revisit_remind_at]': '2018-09-14 19:00',
            'opportunity[note]': '',
            'opportunity[user_id]': self.user.getMyUserId(),  # ,"2222396"
            'opportunity[want_department_id]': str(self.testGetDepartment.getDepartmentId()[0])  # 5168
        }
        response = self.common.post_response_json(url, body, '撤销之后重新提交商机审批' )

    #新增任务
    def add_event_for_opportunitie(self, opportunity_id):
        url = self.base_url + 'events/new?ajax_back_to=%2Fevents%3Fentity_id%3D'+str(opportunity_id)+'%26entity_klass%3DOpportunitie&entity_id='+str(opportunity_id)+'&entity_klass=Opportunitie'
        params = {}
        self.common.get_response_json(url, params, '商机详情页新增任务打开窗口')
        url = self.base_url + 'api/events'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'event[note]':'打电话给客户',
            'event[remind_at]': self.common.get_today_str_yymmddhhmm(),
            'event[remind_type]':'punctual',
            'event[related_item_id]':str(opportunity_id),
            'event[related_item_type]':'Lead',
            'event[user_ids]': str(self.user.getUserId()[0])
        }
        response = self.common.post_response_json(url, params, '给单个商机新增任务')
        event_id = response.json()['data']['id']
        return event_id