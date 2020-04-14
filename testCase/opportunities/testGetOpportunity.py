# -*- coding: utf-8 -*-
__author__ = 'Jun'

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

class GetOpportunities:
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
        self.customer_id = ''
        self.opportunities_id =[]
        self.opportunities_id1 = ''
        self.opportunity_id = ''
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
        self.scope = ''
       # 某些post或是get时要求header里带的信息，应该是一个帐户对应于唯一一个
        # 格式类似于：'Token token=cb5e0c1db161fe92a7f4ce67754821, uid=b9d28be2d18075de7435'
        pass

    #获得所有的我的商机，我协作的商机，我的商机来查询 获取   Obtain
    def opportunities_get_scopes(self):
        url = self.base_url + 'opportunities'
        params = {
            'scope': 'all_own',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取商机页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"opportunities\?scope=(.*?)\">",str(soup))
        return scopes

    def opportunitie(self, opportunity_id):
        # soup = self.get_opportunitie(opportunity_id)
        # self.opportunities_revisit_logs(soup, opportunity_id)
        self.get_opportunitie_detail(opportunity_id)
        self.get_expenses(opportunity_id)
        self.get_events(opportunity_id)
        self.get_attachment(opportunity_id)
        self.get_operation_logs(opportunity_id)
        # self.get_opportunitie(opportunity_id)
        # self.export_selected_opportunities(scope)
        # self.export_all_opportunities(scope)
        # self.opportunities_revisit_logs(soup, opportunity_id)
        self.get_opportunitie_detail(opportunity_id)
        self.get_invoiced_payments_tab(opportunity_id)
        self.opportunitie_add_received_payments(opportunity_id)
        self.get_received_payments_tab(opportunity_id)
        self.get_tab_products(opportunity_id)
        self.get_attachment(opportunity_id)
        self.get_events(opportunity_id)
        self.get_operation_logs(opportunity_id)




    #获取商机ID
    def opportunity_ids(self):
        url = self.base_url + 'opportunities'
        body = {
            'order':'asc',
            'scope':'all_own',
            'sort': 'opportunities.updated_at desc',
            'per_page':10,
            'type':'advance',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的商机')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        #print S
        soup = BeautifulSoup(S, "html.parser")
        checked_opportunitie = soup.find(attrs={'data-entity-table-name':'opportunitie'})
        if checked_opportunitie:
            a = str(checked_opportunitie)
            opportunity_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return opportunity_id_list

    #导出所选商机
    def export_selected_opportunities(self, scope):
        opportunity_ids = self.opportunity_ids()
        url = self.base_url + 'opportunities?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope='+scope+'&amp;sort=opportunities.updated_at+desc&amp;type=advance&selected_ids%5B%5D='+opportunity_ids[0]+'&selected_ids%5B%5D='+opportunity_ids[1]+'&format=js'
        self.common_get_resonse_json(url, 'export_selected_opportunities')
        url = self.base_url + 'opportunities.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&selected_ids%5B%5D='+opportunity_ids[0]+'&selected_ids%5B%5D='+opportunity_ids[1]+'&sort=opportunities.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export selected file')
    #导出全部商机
    def export_all_opportunities(self, scope):
        url = self.base_url + 'opportunities?format_type=calculate_export_pages&order=asc&per_page=10&scope='+scope+'&sort=opportunities.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'export_all_opportunities')

        #点击下载文档
        url = self.base_url + 'opportunities?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&sort=opportunities.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export all opportunitie file')

    #获取单个商机详情
    def get_opportunitie(self, opportunity_id):
        print(opportunity_id)
        url = self.base_url + 'opportunities/'+ str(opportunity_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前用户详情')
        if response !='False':
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        #
        # url = self.base_url + 'opportunities/'+ str(opportunity_id) + '?tab=tab_base'
        params = {
            'tab': 'tab_base'
        }
        self.common.get_response_json(url, params, '商机的基本资料')

    # 获取商机审批状态
    def opportunities_info(self, opportunities_id):
        url = self.base_url + 'opportunities?scope=all_own&per_page=10&type=advance&section_only=true'
        body = {}
        response = self.common.get_response_json(url, body, 'opportunities_info')
        if not response:
            return {}
        html_str = response.content
        # print (html_str)
        soup = BeautifulSoup(html_str, "html.parser")
        a = soup.find(attrs={'data-id': opportunities_id})
        b = a.find(attrs={'data-column': 'approve_status_i18n'})
        c = b.find('div').text
        c = c.strip()
        return c


    #商机写跟进
    def opportunities_revisit_logs(self, soup, opportunity_id):
        status_list = re.findall(r"data-status=\"(.*?)\">",str(soup))
        if status_list:
            for status in status_list:
                url = self.base_url + 'api/opportunities/%s/revisit_logs' %opportunity_id
                body = {
                    'utf8':'✓',
                    'authenticity_token': self.csrf,
                    'revisit_log[category]':'91160',
                    'revisit_log[real_revisit_at]':self.common.get_today_str_yymmddhhmm(),
                    'revisit_log[content]':'写跟进%s' %self.common.get_random_int(9999),
                    'revisit_log[loggable_attributes][status]':status,
                    'revisit_log[loggable_attributes][id]':opportunity_id,
                    'revisit_log[remind_at]':self.common.get_tomorrow_srt_yymmddhhmm()
                }
                response = self.common.post_response_json(url, body, '商机写跟进')
                if not response:
                    return {}

    #查看商机详情
    def get_opportunitie_detail(self, opportunity_id):
        url = self.base_url + 'opportunities/'+ str(opportunity_id)
        params = {
            'only_base_info': 'true'
        }
        self.common.get_response_json(url, params, '获取商机的详细资料')

    # 商机详情页获取联系人tab

    # 商机详情页获取合同tab

    # 商机详情合同tab下新增合同


    #查看商机关联的产品
    def get_tab_products(self,opportunity_id):
        url = self.base_url + str(opportunity_id) +'?tab=tab_products'
        params = {
            'tab': 'tab_products'
        }
        self.common.get_response_json(url, params, '获取商机详情的产品tab页')

    #查看商机的费用
    def get_expenses(self, opportunity_id):
        url = self.base_url + 'api/expenses'
        params = {
            'page': '',
            'perPage': 100,
            'opportunity_id': opportunity_id
        }
        self.common.get_response_json(url, params, '获取当前商机的费用')

    #查看商机的任务
    def get_events(self, opportunity_id):
        url = self.base_url + 'events'
        params = {
            'entity_id': opportunity_id,
            'entity_klass': 'opportunitie'
        }
        self.common.get_response_json(url, params, '获取当前商机的任务')

    #查看商机下的附件
    def get_attachment(self, opportunity_id):
        url = self.base_url + 'api/attachments'
        params = {
            'page':'',
            'perPage':15,
            'entity_id':opportunity_id,
            'klass':'opportunitie'
        }
        self.common.get_response_json(url, params, '获取当前商机的附件')

    #查看商机的操作日志
    def get_operation_logs(self, opportunity_id):
        url = self.base_url + 'api/operation_logs'
        params = {
            'page':'',
            'perPage':15,
            'loggable_id':opportunity_id,
            'loggable_type':'opportunitie'
        }
        self.common.get_response_json(url, params, '查看商机的操作日志')

    #返回到商机详情（基本信息tab）
    def get_opportunities_tab_base(self,opportunity_id):
        url = self.base_url + 'opportunities/'+ str(opportunity_id) + '?tab=tab_base'
        params = {
            'tab': 'tab_base'
        }
        self.common.get_response_json(url, params, '切换回商机的基本资料')

    # 获取商机销售阶段id
    def get_opportunities_stage(self):
        url = self.base_url + 'opportunities/new?event_name=crmListAdd'
        params = {
        }
        self.common.get_response_json(url, params, '获取商机销售阶段id')
        print (self.response.text)

