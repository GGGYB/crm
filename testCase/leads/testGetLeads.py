# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.departments.testGetDepartment import GetDepartment
from testCase.users import testGetUser as users

class GetLeads:
    def __init__(self, cookie, csrf):
        #'https://e.ikcrm.com/
        # self.base_url = base_url
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.testGetDepartment = GetDepartment(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.csrf = csrf
        self.cookie = cookie
        pass

    #获得所有的我的线索，我下属的线索，我的线索来查询 获取线索tab
    def get_all_scope(self):
        url = self.base_url + 'leads/'
        params = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取线索页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"leads\?scope=(.*?)\">",str(soup))
        return scopes

    #线索查重
    def duplicate_leads(self):
        url = self.base_url + 'duplicate'
        params = {
            'add': 'yes',
            'key': 'lead'
        }
        self.common.get_response_json(url, params, '打开线索查重')
        url = self.base_url + 'duplicate/search'
        params = {
            'key': 'lead',
            'query': '1323234'
        }
        response = self.common.get_response_json(url, params, '线索查重')
        #To Be Done 查重没有数据之后新增线索
        if response:
            print ("Lead's duplication  is passed!")
        else:
            print ("Sorry, Lead's duplication is fialed!")

    # 获取当前页的lead_id
    def lead_ids(self):
        url = self.base_url + 'leads'
        body = {
            'order': 'asc',
            'scope': 'all_own',
            'sort': 'leads.updated_at desc',
            'per_page': 10,
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的线索')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, "html.parser")
        # print(soup)
        checked_lead = soup.find(attrs={'data-entity-table-name': 'lead'})
        if checked_lead:
            a = str(checked_lead)
            lead_id_list = re.findall(r"data-id=\"(.*?)\">", a)
            return lead_id_list

    # 导出所选线索
    def export_selected_leads(self, scope):
        lead_ids = self.lead_ids()
        url = self.base_url + 'leads?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope=' + scope + '&amp;sort=leads.updated_at+desc&amp;type=advance&selected_ids%5B%5D=' + \
              lead_ids[0] + '&selected_ids%5B%5D=' + lead_ids[1] + '&format=js'
        self.common_get_resonse_json(url, 'export_selected_leads')
        url = self.base_url + 'leads.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope=' + scope + '&selected_ids%5B%5D=' + \
              lead_ids[0] + '&selected_ids%5B%5D=' + lead_ids[
                  1] + '&sort=leads.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export selected file')

    # 导出全部线索
    def export_all_leads(self, scope):
        url = self.base_url + 'leads?format_type=calculate_export_pages&order=asc&per_page=10&scope=' + scope + '&sort=leads.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'export_all_leads')

        # 点击下载文档
        url = self.base_url + 'leads?export_page=1&format_type=xlsx&order=asc&per_page=10&scope=' + scope + '&sort=leads.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export all lead file')

    # 获取单个线索详情
    def get_lead(self, lead_id):
        url = self.base_url + 'leads/' + str(lead_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前线索详情')
        if response != False:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup



    #查看线索的任务
    def get_events(self, lead_id):
        url = self.base_url + 'events?entity_id='+str(lead_id)+'&entity_klass=Lead'
        params = {
            'entity_id': lead_id,
            'entity_klass': 'Lead'
        }
        self.common.get_response_json(url, params, '获取当前线索的任务')

    #查看线索下的附件
    def get_attachment(self, lead_id):
        url = self.base_url + 'api/attachments?page=&perPage=15&entity_id='+str(lead_id)+'&klass=Lead&sub_type=file'
        params = {
            'page':'',
            'perPage':15,
            'entity_id':lead_id,
            'klass':'Lead'
        }
        self.common.get_response_json(url, params, '获取当前线索的附件')

    #查看线索的操作日志
    def get_operation_logs(self, lead_id):
        url = self.base_url + 'api/operation_logs?page=&perPage=15&loggable_id='+str(lead_id)+'&loggable_type=Lead'
        params = {
            'page':'',
            'perPage':15,
            'loggable_id':lead_id,
            'loggable_type':'Lead'
        }
        self.common.get_response_json(url, params, '查看线索的操作日志')
