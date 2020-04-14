# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class GetCustomers:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.username = ''
        self.password = ''
        self.response = ''
        self.csrf1 = ''
        self.given_cookie = ''  # 用于存储人工指定的cookie，一旦设置后，就不使用页面内获取的cookie
        self.authorization = ''
        self.lead_ids = []
        self.user_id = ''
        self.customers_id =[]
        self.customers_id1 = ''
        self.customer_id = ''
        self.sql_host = 'rdscbq34656z0ix59br0.mysql.rds.aliyuncs.com'
        self.products_id = ''
        self.expense_id = ''
        self.expense_id_list = []
        self.expense_accounts_id = ''
        self.payment_id_list = []
        self.payslip_stats_list = []
        self.commission_rules_id = []
        self.performance_indicator_id  = ''
        self.stations_id = ''
        self.revisit_logs_list = []
        self.payslip_stats_list = []
        self.commission_rules_id = []
        self.performance_indicator_id  = ''
        self.stations_id = ''
        self.revisit_logs_list = []
        self.users_id = []
       # 某些post或是get时要求header里带的信息，应该是一个帐户对应于唯一一个
       # 格式类似于：'Token token=cb5e0c1db161fe92a7f4ce67754821, uid=b9d28be2d18075de7435'
        pass

    #获得所有的我的客户，我协作的客户，我的客户来查询
    def customers_get_scopes(self):
        url = self.base_url + 'customers'
        params = {
            'scope': 'all_own',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取客户页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        navs = soup.findAll(attrs={'class': 'nav-link'})
        scopes = re.findall(r"customers\?scope=(.*?)\">", str(navs))
        return scopes

    def customer(self, customer_id):
        soup = self.get_customer(customer_id)
        self.customers_revisit_logs(soup, customer_id)
        self.get_customer_detail(customer_id)
        self.get_children_customer(customer_id)
        self.get_contacts_belong_customer(customer_id)
        self.get_opportunities_belong_customer(customer_id)
        self.get_contract_belong_customer(customer_id)
        self.get_expenses(customer_id)
        self.get_events(customer_id)
        self.get_attachment(customer_id)
        self.get_operation_logs(customer_id)
    #客户查重
    def customers_dulicate(self, query):
        for duplicate_key in const.DUPLICATE:
            url = self.base_url + 'duplicate/search'
            params = {
                'key': duplicate_key,
                'query': query
            }
            self.common.get_response_json(url, params, '查重的键是'+duplicate_key+', ')
        response = self.common.get_response_json(url, params, '线索查重')
        #To Be Done 查重没有数据之后新增线索
        if response:
            print ("Customer's duplication  is passed!")
        else:
            print ("Sorry, Customer's duplication is fialed!")

    #Common get json
    def common_get_resonse_json(self, url, content):
        body = {}
        response = self.common.get_response_json(url, body, content)
        if not response:
            return {}
        else:
            return response

    #获取当前页的Customer id
    def customer_ids(self):
        url = self.base_url + 'customers'
        body = {
            'order':'asc',
            'scope':'all_own',
            'sort': 'customers.updated_at desc',
            'per_page':10,
            'type':'advance',
            'section_only':'true'
        }
        #print body
        response = self.common.get_response_json(url, body, '获取当前页的客户')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        #print S
        soup = BeautifulSoup(S, "html.parser")
        checked_customer = soup.find(attrs={'data-entity-table-name':'Customer'})
        if checked_customer:
            a = str(checked_customer)
            customer_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return customer_id_list

    #导出所选客户
    def export_selected_customers(self, scope):
        customer_ids = self.customer_ids()
        url = self.base_url + 'customers?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope='+scope+'&amp;sort=customers.updated_at+desc&amp;type=advance&selected_ids%5B%5D='+customer_ids[0]+'&selected_ids%5B%5D='+customer_ids[1]+'&format=js'
        self.common_get_resonse_json(url, 'export_selected_customers')
        url = self.base_url + 'customers.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&selected_ids%5B%5D='+customer_ids[0]+'&selected_ids%5B%5D='+customer_ids[1]+'&sort=customers.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export selected file')
    #导出全部客户
    def export_all_customers(self, scope):
        url = self.base_url + 'customers?format_type=calculate_export_pages&order=asc&per_page=10&scope='+scope+'&sort=customers.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'export_all_customers')

        #点击下载文档
        url = self.base_url + 'customers?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&sort=customers.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export all customer file')

    #获取单个客户详情
    def get_customer(self, customer_id):
        url = self.base_url + 'customers/'+ str(customer_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前用户详情')
        if response !=False:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
    #客户写跟进
    def customers_revisit_logs(self, soup, customer_id):
        status_list = re.findall(r"data-status=\"(.*?)\">",str(soup))
        if status_list:
            for status in status_list:
                url = self.base_url + 'api/customers/%s/revisit_logs' %customer_id
                body = {
                    'utf8':'✓',
                    'authenticity_token': self.csrf,
                    'revisit_log[category]':'91160',
                    'revisit_log[real_revisit_at]':self.common.get_today_str_yymmddhhmm(),
                    'revisit_log[content]':'写跟进 wl-auto%s' %self.common.get_random_int(9999),
                    'revisit_log[loggable_attributes][status]':status,
                    'revisit_log[loggable_attributes][id]':customer_id,
                    'revisit_log[remind_at]':self.common.get_tomorrow_srt_yymmddhhmm()
                }
                response = self.common.post_response_json(url, body, '客户写跟进')
                if not response:
                    return {}

    #查看客户资料
    def get_customer_detail(self, customer_id):
        url = self.base_url + 'customers/'+ str(customer_id)
        params = {
            'only_base_info': 'true'
        }
        self.common.get_response_json(url, params, '获取客户的详细资料')

    #查看客户的下级客户
    def get_children_customer(self, customer_id):
        url = self.base_url + 'api/customers/children?page=&perPage=15&parent_id='+ str(customer_id)
        params = {
            'page':'',
            'perPage':15,
            'parent_id':customer_id
        }
        self.common.get_response_json(url, params, '获取当前客户的下级客户')

    #查看客户的联系人
    def get_contacts_belong_customer(self, customer_id):
        url = self.base_url + 'api/contacts'
        params = {
            'page':'',
            'perPage':15,
            'customer_id':customer_id
        }
        self.common.get_response_json(url, params, '获取当前客户的联系人')

    #查看客户的商机
    def get_opportunities_belong_customer(self, customer_id):
        url = self.base_url + 'api/opportunities?page=&perPage=15&customer_id='+ str(customer_id)
        params = {
            'page':'',
            'perPage':15,
            'customer_id':customer_id
        }
        self.common.get_response_json(url, params, '获取当前客户的商机')

    #查看客户下面的合同
    def get_contract_belong_customer(self, customer_id):
        url = self.base_url + 'api/contracts?page=&perPage=15&customer_id='+ str(customer_id)
        params = {
            'page':'',
            'perPage':15,
            'customer_id':customer_id
        }
        self.common.get_response_json(url, params, '获取当前客户的费用')

    #查看客户的费用
    def get_expenses(self, customer_id):
        url = self.base_url + 'api/expenses'
        params = {
            'page': '',
            'perPage': 100,
            'customer_id': customer_id
        }
        self.common.get_response_json(url, params, '获取当前客户的费用')

    #查看客户的任务
    def get_events(self, customer_id):
        url = self.base_url + 'events'
        params = {
            'entity_id': customer_id,
            'entity_klass': 'Customer'
        }
        self.common.get_response_json(url, params, '获取当前客户的任务')

    #查看客户下的附件
    def get_attachment(self, customer_id):
        url = self.base_url + 'api/attachments'
        params = {
            'page':'',
            'perPage':15,
            'entity_id':customer_id,
            'klass':'Customer'
        }
        self.common.get_response_json(url, params, '获取当前客户的附件')

    #查看客户的操作日志
    def get_operation_logs(self, customer_id):
        url = self.base_url + 'api/operation_logs'
        params = {
            'page':'',
            'perPage':15,
            'loggable_id':customer_id,
            'loggable_type':'Customer'
        }
        self.common.get_response_json(url, params, '查看客户的操作日志')