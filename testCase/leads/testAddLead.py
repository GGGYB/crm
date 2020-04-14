# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from testCase.users import testGetUser as users
from testCase.departments import testGetDepartment as departmentid

class AddLead:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.customers_id =[]
        self.params = ''
        self.user = users.GetUser(cookie, csrf)
        self.DepartmentId = departmentid.GetDepartment(cookie, csrf)
        pass

    #新增线索
    def add_lead(self):
        url = self.base_url + 'api/leads'
        body = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'refer_call_record_id':'',
            'lead[id]':'',
            'lead[name]':'线索名2222222222222称%s' %self.common.get_today_str_yymmddhhmm(),
            'lead[company_name]': '公司名称%s' %self.common.get_random_int(99999999),
            'lead[department]':'',
            'lead[job]':'',
            'lead[address_attributes][tel]':'13232342324',
            'lead[address_attributes][phone]':'',
            'lead[address_attributes][wechat]':'',
            'lead[address_attributes][qq]':'',
            'lead[address_attributes][wangwang]':'',
            'lead[address_attributes][email]':'',
            'lead[address_attributes][url]':'www.baidu.com',
            'china_tag_id':'4',
            'lead[address_attributes][country_id]':'4',
            'lead[address_attributes][province_id]':'',
            'lead[address_attributes][city_id]':'',
            'lead[address_attributes][district_id]':'',
            'lead[address_attributes][detail_address]':'',
            'lead[address_attributes][zip]':'',
            'lead[file_asset_f6f989][attachment_ids][]':'',
            'lead[file_asset_f6f989][attachment_ids][]':'33177',
            'lead[file_asset_f6f989][attachment_ids][]':'33178',
            'lead[status]'
            'lead[source]':'',
            'lead[revisit_remind_at]':'',
            'lead[note]':'',
            'lead[text_asset_4281ae]':'',
            'lead[text_asset_49ed60]':'',
            'lead[text_asset_74a75f]':'',
            'lead[text_area_asset_a567a5]':'',
            'lead[numeric_asset_80c6ec]':'',
            'lead[numeric_asset_64d75e]':'',
            'lead[numeric_asset_366270]':'',
            'lead[file_asset_2f66d7][attachment_ids][]':'',
            'lead[datetime_asset_3cbb87]':'',
            'lead[text_asset_0f9c58]':'',
            'lead[text_asset_8c4b40][]':'',
            'lead[user_id]': self.user.getMyUserId(),
            'lead[want_department_id]':self.DepartmentId.getDepartmentId()
        }
        response = self.common.post_response_json(url, body, '新增线索是'+url)
        if not response:
            return {}
        self.response = response
        lead_id = self.response.json()['data']['id']
        return lead_id
    #扫描名片
    def leads_camcard_launch(self):
        url = self.base_url + 'leads/camcard_launch'
        body = {}
        self.common.get_response_json(url, body, '打开扫描名片窗口')
        #开始扫描
        url = self.base_url + 'leads/camcard_explain'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'attachment_id':'33272'
        }
        self.common.post_response_json(url, params, '线索-扫描名片添加图片')
        #开始添加线索
        url = self.base_url + 'api/leads/camcard'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'attachment_id':'33276',
            'entity_attributes[name]':'线索名称%s' %self.common.get_random_int(99999999),
            'entity_attributes[company_name]':'扫描名片添加线索%s' %self.common.get_random_int(99999999),
            'entity_attributes[department]':'',
            'entity_attributes[job]':'',
            'entity_attributes[address_attributes][tel]':'',
            'entity_attributes[address_attributes][phone]':'',
            'entity_attributes[address_attributes][email]':'',
            'entity_attributes[address_attributes][qq]':'',
            'entity_attributes[address_attributes][fax]':'',
            'entity_attributes[address_attributes][url]':'',
            'entity_attributes[address_attributes][detail_address]':'',
            'entity_attributes[address_attributes][zip]':''
        }
        self.common.post_response_json(url, params, '扫描名片添加线索')

    #新增任务
    def add__event_for_lead(self, lead_id):
        url = self.base_url + 'events/new?ajax_back_to=%2Fevents%3Fentity_id%3D111662%26entity_klass%3DLead&entity_id='+str(lead_id)+'&entity_klass=Lead'
        params = {}
        self.common.get_response_json(url, params, '线索详情页新增任务打开窗口')
        url = self.base_url + 'api/events'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'event[note]':'打电话给客户',
            'event[remind_at]': self.common.get_today_str_yymmddhhmm(),
            'event[remind_type]':'punctual',
            'event[related_item_id]':str(lead_id),
            'event[related_item_type]':'Lead',
            'event[user_ids]': str(self.user.getMyUserId())
        }
        response = self.common.post_response_json(url, params, '给单个线索新增任务')
        id = response.json()['data']['id']
