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
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class AddContract:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.user = users.GetUser(cookie, csrf)
        self.contracts_id =''
        self.params = ''
        self.contract_id = ''
        # self.DepartmentId = self.DepartmentId.getDepartmentId()
        # pass

    # 新增合同（关闭审批）
    def add_contracts(self,sign_date ='2018-07-22',total_amount= 2000,approve_status='approved',DepartmentId=0):
        # customer_id = self.testAddCustomer.add_customers()
        customer_id = 1228332
        url = self.base_url + 'api/contracts'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'refer_call_record_id': '',
            'request_ticket':  self.common.get_random_int(999999999),
            'contract[id]': '',
            'contract[approve_status]': approve_status,
            'contract_action_name': 'new',
            'contract[title]': 'contracts%s' % self.common.get_today_str_yymmddhhmm(),
            'contract[customer_id]': customer_id,
            'contract[total_amount]': total_amount,
            'contract[sign_date]': sign_date,
            'contract[start_at]': '2018-06-30',
            'contract[end_at]': '2018-08-30',
            'contract[opportunity_id]': '',
            'contract[received_payment_plans_attributes][][id]':'',
            'contract[received_payment_plans_attributes][][receive_stage]': '1',
            'contract[received_payment_plans_attributes][][receive_date]': '2019-01-22',
            'contract[received_payment_plans_attributes][][amount]': '100',
            'contract[received_payment_plans_attributes][][received_types]': '268979',
            'contract[received_payment_plans_attributes][][note]':'',
            'contract[status]': '',
            'contract[sn]':'',
            'contract[special_terms]':'',
            'contract[category]':'',
            'contract[payment_type]':'',
            'contract[customer_signer]':'',
            'contract[our_signer]':'',
            'contract[revisit_remind_at]':'',
            'contract[note]':'',
            'contract[user_id]': self.user.getMyUserId(),
            'contract[want_department_id]': self.DepartmentId.getDepartmentId()[DepartmentId]

        }
        # print (body)
        response = self.common.post_response_json(url, body, '新增合同 api是'+url)
        if not response:
            return {}
        self.response = response
        # print(self.response.json())
        contract_id = self.response.json()['data']['id']
        # print (contract_id)
        return contract_id,customer_id

    #新增待审批合同
    def add_applying_contract(self):
        url = self.base_url + 'api/contracts'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'refer_call_record_id': '',
            'request_ticket': 'edb57235-246e-4776-a85f-b658cd4e668e',
            'contract[id]': '',
            'contract[approve_status]': 'applying',
            'contract_action_name': 'new',
            'contract[title]': 'contracts%s' % self.common.get_random_int(99999999),
            'contract[customer_id]': self.testAddCustomer.add_customers(),
            'contract[total_amount]': '20000',
            'contract[sign_date]': '2018-06-30',
            'contract[start_at]': '2018-06-30',
            'contract[end_at]': '2018-08-30',
            'contract[opportunity_id]': '',
            'contract[product_assets_attributes][][id]': '',
            'contract[product_assets_attributes][][_destroy]': 'false',
            'contract[product_assets_attributes][][product_id]': '',
            'contract[product_assets_attributes][][recommended_unit_price]': '',
            'contract[product_assets_attributes][][quantity]': '',
            'contract[product_assets_attributes][][remark]': '',
            'contract[product_assets_attributes][][product_attr_id]': '',
            'contract[status]': '',
            'contract[sn]': '',
            'contract[special_terms]': '',
            'contract[category]': '',
            'contract[payment_type]': '',
            'contract[customer_signer]': '',
            'contract[our_signer]': '',
            'contract[revisit_remind_at]': '',
            'contract[note]': '',
            'contract[user_id]': self.user.getMyUserId(),
            'contract[want_department_id]': self.DepartmentId.getDepartmentId()
        }
        response = self.common.post_response_json(url, body, '开启审批新增合同 api是'+url)
        if not response:
            return {}
        self.response = response
        # print(self.response.json())
        contract_id = self.response.json()['data']['id']
        self.contract_id = contract_id
        return contract_id


    #新增合同关联产品
    def add_contracts_products_add(self,goods_id_list=[11012,11013],quantity_list=[[0],[1]],price_list=[[0],[1]],product_name_list=['测试产品01','测试产品02'],total_amount= 5000,sign_date = '2019-01-12',start_at='2018-12-21',approve_status = 'approved',DepartmentId=0):
        url = self.base_url + 'api/contracts'
        if len(goods_id_list) != len(quantity_list):
            print (u'产品数组与数量数组不一致，请修改！')
            return
        if len(goods_id_list) != len(price_list):
            print (u'产品数组与价格数组不一致，请修改！')
            return
        product_assets_attributes = []
        for i in range(len(goods_id_list)):
            product_info = {
                        'product_id': goods_id_list[i],
                        'recommended_unit_price':price_list[i],
                        'quantity': quantity_list[i],
                        'product_attr_id':'',
                        'product_name_list':product_name_list[i],
            }
            product_assets_attributes.append(product_info)
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'contract_action_name': 'new',
            'contract':{
                'product_assets_attributes':[

                ],
                'approve_status': approve_status,
                'id': '',
                'title': '合同%s' % self.common.get_random_int(99999999),
                'customer_id': self.testAddCustomer.add_customers(),
                'opportunity_id': '',
                'total_amount': total_amount,
                'sign_date': sign_date,
                'start_at': start_at,
                'end_at': '',
                'status':'',
                'sn': '',
                'category': '',
                'payment_type': '',
                'customer_signer': '',
                'our_signer': '',
                'revisit_remind_at': '',
                'special_terms': '',
                'user_id': self.user.getMyUserId(),
                'want_department_id': self.DepartmentId.getDepartmentId()[DepartmentId]
            }
        }
        body['contract']['product_assets_attributes'] =  product_assets_attributes
        response = self.common.post_json_response_json(url, body, 'add contracts')
        if not response:
            return {}
        self.response = response
        contract_id = self.response.json()['data']['id']
        self.contract_id = contract_id
        return contract_id

    #
    # #新增待审批合同关联产品
    # def add_applying_contracts_products_add(self, goods_id_list=[11012,11013],quantity_list=[[0],[1]],price_list=[[0],[1]],product_name_list=['测试产品01','测试产品02'],total_amount= 5000,sign_date = '2019-01-12',start_at='2018-12-21',approve_status = 'applying',DepartmentId=0):
    #     url = self.base_url + 'api/contracts'
    #     if len(goods_id_list) != len(quantity_list):
    #         print (u'产品数组与数量数组不一致，请修改！')
    #         return
    #     if len(goods_id_list) != len(price_list):
    #         print (u'产品数组与价格数组不一致，请修改！')
    #         return
    #     product_assets_attributes = []
    #     for i in range(len(goods_id_list)):
    #         product_info = {
    #                     'product_id': goods_id_list[i],
    #                     'recommended_unit_price':price_list[i],
    #                     'quantity': quantity_list[i],
    #                     'product_attr_id':'',
    #                     'product_name_list':product_name_list[i],
    #         }
    #         product_assets_attributes.append(product_info)
    #     body = {
    #         'utf8': '✓',
    #         'authenticity_token': self.csrf,
    #         'contract_action_name': 'new',
    #         'contract':{
    #             'product_assets_attributes':[
    #
    #             ],
    #             'approve_status': approve_status,
    #             'id': '',
    #             'title': '合同%s' % self.common.get_random_int(99999999),
    #             'customer_id': self.testAddCustomer.add_customers(),
    #             'opportunity_id': '',
    #             'total_amount': total_amount,
    #             'sign_date': sign_date,
    #             'start_at': start_at,
    #             'end_at': '',
    #             'status':'',
    #             'sn': '',
    #             'category': '',
    #             'payment_type': '',
    #             'customer_signer': '',
    #             'our_signer': '',
    #             'revisit_remind_at': '',
    #             'special_terms': '',
    #             'contract[user_id]': self.user.getMyUserId(),
    #             'contract[want_department_id]': self.DepartmentId.getDepartmentId()[DepartmentId]
    #         }
    #     }
    #     body['contract']['product_assets_attributes'] =  product_assets_attributes
    #     response = self.common.post_json_response_json(url, body, 'add contracts')
    #     if not response:
    #         return {}
    #     self.response = response
    #     contract_id = self.response.json()['data']['id']
    #     self.contract_id = contract_id
    #     return contract_id
    #
    # #新增合同草稿关联产品
    # def add_contracts_draft_products_add(self, goods_id_list=[11012,11013],quantity_list=[[0],[1]],price_list=[[0],[1]],product_name_list=['测试产品01','测试产品02'],total_amount= 5000,sign_date = '2019-01-12',approve_status='draft',DepartmentId=0):
    #     url = self.base_url + 'api/contracts'
    #     if len(goods_id_list) != len(quantity_list):
    #         print (u'产品数组与数量数组不一致，请修改！')
    #         return
    #     if len(goods_id_list) != len(price_list):
    #         print (u'产品数组与价格数组不一致，请修改！' )
    #         return
    #     product_assets_attributes = []
    #     for i in range(len(goods_id_list)):
    #         product_info = {
    #                     'product_id': goods_id_list[i],
    #                     'recommended_unit_price':price_list[i],
    #                     'quantity': quantity_list[i],
    #                     'product_attr_id':'' ,
    #                     'product_name_list':product_name_list[i],
    #         }
    #         product_assets_attributes.append(product_info)
    #     body = {
    #         'utf8': '✓',
    #         'authenticity_token': self.csrf,
    #         'contract_action_name': 'new',
    #         'contract':{
    #             'product_assets_attributes':[
    #
    #             ],
    #             'approve_status': approve_status,
    #             'id': '',
    #             'title': '合同%s' % self.common.get_random_int(99999999),
    #             'customer_id': self.testAddCustomer.add_customers(),
    #             'opportunity_id': '',
    #             'total_amount': total_amount,
    #             'sign_date': sign_date,
    #             'start_at': '',
    #             'end_at': '',
    #             'status': '',
    #             'sn': '',
    #             'category': '',
    #             'payment_type': '',
    #             'customer_signer': '',
    #             'our_signer': '',
    #             'revisit_remind_at': '',
    #             'special_terms': '',
    #             'contract[user_id]': self.user.getMyUserId(),
    #             'contract[want_department_id]': self.DepartmentId.getDepartmentId()[DepartmentId]
    #         }
    #     }
    #     body['contract']['product_assets_attributes'] =  product_assets_attributes
    #     response = self.common.post_json_response_json(url, body, 'add contracts')
    #     if not response:
    #         return {}
    #     self.response = response
    #     contract_id = self.response.json()['data']['id']
    #     self.contract_id = contract_id
    #     return contract_id
    #

    #新增任务
    def add_event_for_contract(self, contract_id):
        url = self.base_url + 'events/new?ajax_back_to=%2Fevents%3Fentity_id%3D'+str(contract_id)+'%26entity_klass%3DContract&entity_id='+str(contract_id)+'&entity_klass=Contract'
        params = {}
        self.common.get_response_json(url, params, '合同详情页新增任务打开窗口')
        url = self.base_url + 'api/events'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'event[note]':'打电话给客户',
            'event[remind_at]': self.common.get_tomorrow_srt_yymmddhhmm(),
            'event[remind_type]':'punctual',
            'event[related_item_id]':str(contract_id),
            'event[related_item_type]':'Contract',
            'event[user_ids]': str(self.user.getMyUserId())
        }
        # print(params)
        response = self.common.post_response_json(url, params, '给单个合同新增任务')
        event_id = response.json()['data']['id']
        return event_id

    # def contract_approval_two(self, id):
    #     url = self.base_url + 'api/approvals/' + str(id) + '/approve'
    #     body = {
    #         'utf8': '✓',
    #         '_method': 'put',
    #         'authenticity_token': self.csrf,
    #         'key': 'contract',
    #         'contract[step]': '1',
    #         'contract[approve_description]': '',
    #         'contract[notify_user_ids][]': 'contracts%s' % self.common.get_random_int(99999999),
    #         'contract[notify_user_ids][]': '3945',
    #         'contract[notify_user_ids][]': '3971',
    #         'contract[notify_user_ids][]': '3951',
    #         'contract[notify_user_ids][]': '3950',
    #         'contract[notify_user_ids][]': '3989'
    #     }
    #     response = self.common.post_response_xml(url, body, '合同审批通过')
    #     return response
