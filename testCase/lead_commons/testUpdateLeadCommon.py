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
from commons import common
from commons.const import const
from .testGetLeadCommon import GetLeadCommonId
from testCase.users import testGetUser as users


class UpdateLeadCommonId:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.lead_common = GetLeadCommonId(cookie, csrf)
        self.users = users.GetUser(cookie, csrf)
        self.users_id = []
        pass

    def operate_lead_common(self, lead_ids,lead_id):
        self.batch_update_lead_common(lead_ids,lead_id)
        self.massive_transfer_leads_common(lead_ids,lead_id)

    #批量编辑线索池的线索
    def batch_update_lead_common(self, lead_ids,lead_id):
        url = self.base_url + 'batch_edit/field_form?model=LeadCommon&setting_id=' + str(lead_id)
        params = {}
        response = self.common.get_response_json(url, params, '打开批量编辑线索池的线索的页面')
        soup = BeautifulSoup(response.content, 'html.parser')
        optional_field = soup.find(attrs={'id': 'field_choice'})
        fields = re.findall(r"value=\"(.*?)\">", str(optional_field))
        selected_fields = soup.findAll(attrs={'class': 'batch-edit-custom-field hidden'})
        selected_field_list = []
        for i in selected_fields:
            selected_field = re.findall(r"<option value=\"(.*?)\">", str(i))
            selected_field_list.append(selected_field)
        url = self.base_url + 'api/lead_commons/batch_update?common_id=' + str(lead_id)
        params = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'field_choice': fields[2],
            'lead['+fields[2]+']':selected_field_list[1][2],
            'ids[]': lead_ids
        }
        self.common.put_response_json(url, params, '批量编辑线索池里的线索')


    # 批量转移线索
    def massive_transfer_leads_common(self, lead_ids,lead_id):
        url = self.base_url + 'lead_commons/massive_transfer?common_id=2' + str(lead_id)
        body = {}
        self.common.get_response_json(url, body, '打开批量转移线索的窗口')
        #获取用户id
        self.users_id = self.users.getUserId()
        #转移
        url = self.base_url +'api/lead_commons/mass_transfer?common_id=' + str(lead_id)
        params = {
            'authenticity_token':self.csrf,
            'user_id': self.users_id[0],
            'transfer_contracts': 'false',
            'transfer_opportunities': 'false',
            'nowin_opportunities': 'false',
            'lead_ids[]': lead_ids
        }
        self.common.put_response_json(url, params, '批量转移线索池的线索给他人')

    # 批量删除线索池的线索
    def bulk_delete_lead_common(self,  lead_ids,lead_id):
        url = self.base_url + 'lead_commons/bulk_delete?common_id=' + str(lead_id)
        body = {
            'lead_ids[]': lead_ids,
            'authenticity_token': self.csrf
        }
        response = self.common.delete_response_json(url, body, '批量删除线索池的线索')
        if not response:
            return {}

   # 线索池成员抢单个线索
    def take_singel_lead(self,lead_ids):
        url = self.base_url + 'api/leads/' + str(lead_ids[0]) + '/take'
        body = {}
        response = self.common.put_response_json(url,body,'抢单个线索')


    # 线索池成员批量抢线索
    def bulk_take_lead(self,lead_ids,lead_common_id):
        url = self.base_url +'api/leads/bulk_take?common_id=' + str(lead_common_id)
        body = {
            'lead_ids[]': lead_ids[1],
            'authenticity_token': self.csrf
        }
        response = self.common.put_response_json(url,body,'批量抢线索')