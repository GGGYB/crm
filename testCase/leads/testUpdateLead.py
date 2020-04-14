# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import re
from commons import common
from commons.const import const
from testCase.users import testGetUser as users
from  testCase.lead_commons import testGetLeadCommon

class UpdateLeads:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.users = users.GetUser(cookie, csrf)
        self.lead_common_id = testGetLeadCommon.GetLeadCommonId(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.users_id = []
        self.customers_id = []

    # 批量转移线索
    def update_leads_by_scope(self, scope, lead_ids):
        url = self.base_url + 'leads/massive_transfer'
        body = {}
        self.common.get_response_json(url, body, '打开批量转移线索的创窗口')
        #获取用户id
        self.users_id = self.users.getUserId()
        #转移
        url = self.base_url + 'api/leads/mass_transfer'
        params = {
            'authenticity_token':self.csrf,
            'user_id': self.users_id[0],
            'transfer_contracts': 'false',
            'transfer_opportunities': 'false',
            'nowin_opportunities': 'false',
            'lead_ids[]': lead_ids[0],
            'lead_ids[]': lead_ids[1]
        }
        self.common.put_response_json(url, params, '批量转移线索')

    # 批量转移至线索池
    def mass_transfer_to_common_pool(self, lead_ids):
        url = self.base_url + 'api/leads/mass_transfer_to_common_pool'
        body = {
            'common_id':self.lead_common_id.get_lead_common_id(),
            'authenticity_token':self.csrf,
            'lead_ids[]': lead_ids,
        }
        self.common.put_response_json(url,body,'批量转移至线索池')


    #批量编辑线索
    def batch_update_leads(self, scope, lead_ids):
        url = self.base_url + 'batch_edit/field_form?model=Lead'
        params = {}
        response = self.common.get_response_json(url, params, '打开批量编辑线索的页面')
        soup = BeautifulSoup(response.content, 'html.parser')
        optional_field = soup.find(attrs={'id': 'field_choice'})
        fields = re.findall(r"value=\"(.*?)\">", str(optional_field))
        selected_fields = soup.findAll(attrs={'class': 'batch-edit-custom-field hidden'})
        selected_field_list = []
        for i in selected_fields:
            selected_field = re.findall(r"<option value=\"(.*?)\">", str(i))
            selected_field_list.append(selected_field)
        url = self.base_url + 'api/leads/batch_update'
        params = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'field_choice': fields[1],
            'lead['+fields[1]+']':selected_field_list[1][2],
            'ids[]': lead_ids[0],
            'ids[]': lead_ids[1]
        }
        self.common.put_response_json(url, params, '批量编辑线索')

    #快捷编辑线索
    def quick_edit_leads(self, lead_id):
        url = self.base_url + 'quick_edit/field_form?model=Lead&id=111556&field_name=name&page_type=index&_=1521614005045'
        params = {
            'model':'Lead',
            'id':lead_id,
            'field_name':'name',
            'page_type':'index',
        }
        self.common.get_response_json(self, params, '快捷编辑线索获取当前线索的field name')

        url = self.base_url + 'api/leads/' + str(lead_id)
        params = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'lead[id]': lead_id,
            'lead[name]': 'lead name'
        }

    #查重字段
    def check_duplicate_field(self, lead_id):
        url = self.base_url + 'api/leads/check_duplicate_field.json'
        params = {
            'field':'tel',
            'field_value':'132323423245',
            'lead_id':lead_id
        }
        response = self.common.post_response_json(url, params, '查询电话是否重复')

    #写跟进
    def write_revisit_log(self, scope, lead_id):
        url = self.base_url + 'leads/'+str(lead_id)+'/revisit_logs/new'
        params = {}
        self.common.get_response_json(url, params, '打开写跟进窗口')
        url = self.base_url + 'leads/' +str(lead_id)+'/revisit_logs?lead_id='+str(lead_id)
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'revisit_log[category]':'89825',
            'revisit_log[real_revisit_at]':self.common.get_today_str_yymmddhhmm(),
            'revisit_log[content]':'写跟进%s' %self.common.get_random_int(999),
            'revisit_log[loggable_attributes][status]':'89822',
            'revisit_log[loggable_attributes][id]':str(lead_id),
            'revisit_log[remind_at]':''
        }
        self.common.post_response_json(url, params, '线索列表页写跟进')

