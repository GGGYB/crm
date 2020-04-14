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
from testCase.customers.testAddCustomer import AddCustomer
from .testAddContract import AddContract


class GetContracts:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.testAddContract = AddContract(cookie, csrf)
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
        self.contracts_id =[]
        self.contracts_id1 = ''
        self.contracts_id = ''
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
        pass

    #获得所有的我的合同，我协作的合同，我的合同来查询 获取   Obtain
    def contracts_get_scopes(self):
        url = self.base_url + 'contracts'
        params = {
            'scope': 'all_own',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取合同页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"contracts\?scope=(.*?)\">",str(soup))
        # scopes = re.findall(r"hetongs\?scope=(.*?)\">", str(soup))
        return scopes

    def contract(self, contract_id):
        # soup = self.get_contract(contract_id)
        # self.contracts_revisit_logs(soup, contract_id)
        self.get_contract_detail(contract_id)
        self.get_expenses(contract_id)
        self.get_events(contract_id)
        self.get_attachment(contract_id)
        self.get_operation_logs(contract_id)
        # self.get_contract(contract_id)
        # self.export_selected_contracts(scope)
        # self.export_all_contracts(scope)
        # self.contracts_revisit_logs(soup, contract_id)
        self.get_contract_detail(contract_id)
        self.get_invoiced_payments_tab(contract_id)
        self.contract_add_received_payments(contract_id)
        self.get_received_payments_tab(contract_id)
        self.get_tab_products(contract_id)
        self.get_attachment(contract_id)
        self.get_events(contract_id)
        self.get_operation_logs(contract_id)


    #获取合同ID
    def contract_ids(self):
        url = self.base_url + 'contracts'
        body = {
            'order':'asc',
            'scope':'all_own',
            'sort': 'contracts.updated_at desc',
            'per_page':10,
            'type':'advance',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的合同')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        #print S
        soup = BeautifulSoup(S, "html.parser")
        checked_contract = soup.find(attrs={'data-entity-table-name':'contract'})
        if checked_contract:
            a = str(checked_contract)
            contract_id_list = re.findall(r"data-id=\"(.*?)\">",a)
            return contract_id_list

    #导出所选合同
    def export_selected_contracts(self, scope):
        contract_ids = self.contract_ids()
        url = self.base_url + 'contracts?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope='+scope+'&amp;sort=contracts.updated_at+desc&amp;type=advance&selected_ids%5B%5D='+contract_ids[0]+'&selected_ids%5B%5D='+contract_ids[1]+'&format=js'
        self.common_get_resonse_json(url, 'export_selected_contracts')
        url = self.base_url + 'contracts.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&selected_ids%5B%5D='+contract_ids[0]+'&selected_ids%5B%5D='+contract_ids[1]+'&sort=contracts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export selected file')
    #导出全部合同
    def export_all_contracts(self, scope):
        url = self.base_url + 'contracts?format_type=calculate_export_pages&order=asc&per_page=10&scope='+scope+'&sort=contracts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'export_all_contracts')

        #点击下载文档
        url = self.base_url + 'contracts?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&sort=contracts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export all contract file')

    #获取单个合同详情
    def get_contract(self, contract_id):
        print(contract_id)
        url = self.base_url + 'contracts/'+ str(contract_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前用户详情')
        if response !='False':
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        #
        url = self.base_url + 'contracts/'+ str(contract_id) + '?tab=tab_base'
        params = {
            'tab': 'tab_base'
        }
        self.common.get_response_json(url, params, '合同的基本资料')


    #合同写跟进
    def contracts_revisit_logs(self, soup, contract_id):
        status_list = re.findall(r"data-status=\"(.*?)\">",str(soup))
        if status_list:
            for status in status_list:
                url = self.base_url + 'api/contracts/%s/revisit_logs' %contract_id
                body = {
                    'utf8':'✓',
                    'authenticity_token': self.csrf,
                    'revisit_log[category]':'91160',
                    'revisit_log[real_revisit_at]':self.common.get_today_str_yymmddhhmm(),
                    'revisit_log[content]':'写跟进%s' %self.common.get_random_int(9999),
                    'revisit_log[loggable_attributes][status]':status,
                    'revisit_log[loggable_attributes][id]':contract_id,
                    'revisit_log[remind_at]':self.common.get_tomorrow_srt_yymmddhhmm()
                }
                response = self.common.post_response_json(url, body, '合同写跟进')
                if not response:
                    return {}

    #查看合同资料
    def get_contract_detail(self, contract_id):
        url = self.base_url + 'contracts/'+ str(contract_id)
        params = {
            'only_base_info': 'true'
        }
        self.common.get_response_json(url, params, '获取合同的详细资料')

    # 合同获取回款记录tab
    def get_received_payments_tab(self, contract_id):
        # url = self.base_url + str(contract_id) +'?tab=tab_received_payments'
        url = self.base_url +'api/received_payments?page=&perPage=15&contract_id=' + str(contract_id)
        params ={
            'tab': 'tab_received_payments'
        }
        self.common.get_response_json(url, params, '获取合同详情的回款tab页')

    #合同详情页新增回款计划
    def add_received_payment_plans(self,contract_id):
        url = self.base_url + 'contracts/'+ str(contract_id)+'?tab=tab_received_payments'
        params ={
            'tab': 'tab_received_payments'
        }
        url = self.base_url +'api/received_payment_plans/batch_create?contract_id='+ str(contract_id)
        body = {
            'utf8': ' ✓',
            'authenticity_token': self.csrf,
            'plans[0][customer_id]': self.testAddCustomer.add_customers(),
            'plans[0][contract_id]': self.testAddContract.add_contracts(),
            'plans[0][receive_stage]': '1',
            'plans[0][receive_date]': '2018-08-01',
            'plans[0][amount]': '5000',
            'plans[0][note]':'',
            'plans[1][customer_id]': self.testAddCustomer.add_customers(),
            'plans[1][contract_id]': self.testAddContract.add_contracts(),
            'plans[1][receive_stage]': '1',
            'plans[1][receive_date]': '2018-08-01',
            'plans[1][amount]': '6000',
            'plans[1][note]': ''
        }
        response = self.common.post_response_json(url, body, '新增回款计划 api是' + url)
        if not response:
            return {}
        self.response = response
        received_payments_id = self.response.json()['data']['id']
        return received_payments_id

    #合同详情页新增回款记录
    def contract_add_received_payments(self, contract_id):
        url = self.base_url +'/contracts/' +str(contract_id) + '/received_payments'
        body ={
            'authenticity_token':self.csrf,

            'contract_id': 30939,
            'received_payment[receive_date]': '2018-06-22',
            'received_payment[amount]': '2000',
            'received_payment[customer_id]': self.customer_id,
            'received_payment[contract_id]': self.contracts_id,
            'received_payment[received_payment_plan_id]': '',
            'received_payment[payment_type]':'',
            'received_payment[received_types]':'',
            'received_payment[receive_user_id]': self.user_id,
            'received_payment[note]':'备注',
        }
        response = self.common.post_response_json(url, body, '合同详情页新增回款记录 api是'+url)
        if not response:
            return {}
        self.response = response
        received_payments_amount = self.response.json()['data']['amount']
        return received_payments_amount


    # 合同获取开票记录tab
    def get_invoiced_payments_tab(self, contract_id):
        url = self.base_url +'api/invoiced_payments?page=&perPage=15&contract_id=' + str(contract_id)
        params ={
            'tab': 'tab_invoiced_payments'
        }
        self.common.get_response_json(url, params, '获取合同详情的开票tab页')

    #合同详情页新增开票记录
    def contract_add_invoiced_payments(self, contract_id):
        url = self.base_url +'/contracts/' +str(contract_id) + '/invoiced_payments'
        body ={
            'authenticity_token':self.csrf,
            'invoiced_payment[amount]': '2000',
            'invoiced_payment[invoice_types]': '205671',
            'invoiced_payment[invoice_no]':'',
            'invoiced_payment[note]':'备注',
            'invoiced_payment[invoiced_date]': '2018-06-23',
            'invoiced_payment[broker_user_id]': self.user_id,
            'invoiced_payment[content]': '开票' %self.common.get_random_int(99999),
        }
        response = self.common.post_response_json(url, body, '合同详情页新增开票记录 api是'+url)
        if not response:
            return {}
        self.response = response
        invoiced_payment_amount = self.response.json()['data']['amount']
        return invoiced_payment_amount

    #查看合同关联的产品
    def get_tab_products(self,contract_id):
        url = self.base_url + 'api/product_assets?page=&perPage=15&assetable_id='+str(contract_id)+'&assetable_type=Contract'
        print(url)
        params = {
            'tab': 'tab_products'
        }
        self.common.get_response_json(url, params, '获取合同详情的产品tab页')

    #查看合同的费用
    def get_expenses(self, contract_id):
        url = self.base_url + 'api/expenses?page=&perPage=100&contract_id='+str(contract_id)
        params = {
            'page': '',
            'perPage': 100,
            'contract_id': contract_id
        }
        self.common.get_response_json(url, params, '获取当前合同的费用')

    #查看合同的任务
    def get_events(self, contract_id):
        url = self.base_url + 'events?entity_id='+str(contract_id)+'&entity_klass=Contract'
        params = {
            'entity_id': contract_id,
            'entity_klass': 'Contract'
        }
        self.common.get_response_json(url, params, '获取当前合同的任务')

    #查看合同下的附件
    def get_attachment(self, contract_id):
        url = self.base_url + 'api/attachments?page=&perPage=15&entity_id='+str(contract_id)+'&klass=Contract&sub_type=file'
        params = {
            'page':'',
            'perPage':15,
            'entity_id':contract_id,
            'klass':'Contract'
        }
        self.common.get_response_json(url, params, '获取当前合同的附件')

    #查看合同的操作日志
    def get_operation_logs(self, contract_id):
        url = self.base_url + 'api/operation_logs?page=&perPage=15&loggable_id='+str(contract_id)+'&loggable_type=Contract'
        params = {
            'page':'',
            'perPage':15,
            'loggable_id':contract_id,
            'loggable_type':'Contract'
        }
        self.common.get_response_json(url, params, '查看合同的操作日志')

    #返回到合同详情（基本信息tab）
    def get_contracts_tab_base(self,contract_id):
        url = self.base_url + 'contracts/'+ str(contract_id) + '?tab=tab_base'
        params = {
            'tab': 'tab_base'
        }
        self.common.get_response_json(url, params, '切换回合同的基本资料')
