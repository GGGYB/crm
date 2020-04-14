# -*- coding: utf-8 -*-
__author__ = 'Jun'


from bs4 import BeautifulSoup
import re
from commons import common
from commons.const import const
from testCase.users import testGetUser as users

class UpdateContacts:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.users = users.GetUser(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.users_id = []
        self.customers_id = []

    # 批量转移联系人
    def update_contacts_by_scope(self, scope, contact_ids):
        url = self.base_url + 'contacts/massive_transfer'
        body = {}
        self.common.get_response_json(url, body, '打开批量转移联系人的创窗口')
        #获取用户id
        self.users_id = self.users.getUserId()
        #转移
        url = self.base_url + 'api/contacts/mass_transfer'
        params = {
            'authenticity_token':self.csrf,
            'user_id': self.users_id[0],
            'transfer_contracts': 'false',
            'transfer_opportunities': 'false',
            'nowin_opportunities': 'false',
            'contact_ids[]': contact_ids[0],
            'contact_ids[]': contact_ids[1]
        }
        self.common.put_response_json(url, params, '批量转移联系人')

    #批量编辑联系人
    def batch_update_contacts(self, scope, contact_ids):
        url = self.base_url + 'batch_edit/field_form?model=Contact'
        params = {}
        response = self.common.get_response_json(url, params, '打开批量编辑联系人的页面')
        soup = BeautifulSoup(response.content, 'html.parser')
        optional_field = soup.find(attrs={'id': 'field_choice'})
        fields = re.findall(r"value=\"(.*?)\">", str(optional_field))
        selected_fields = soup.findAll(attrs={'class': 'batch-edit-custom-field hidden'})
        selected_field_list = []
        for i in selected_fields:
            selected_field = re.findall(r"<option value=\"(.*?)\">", str(i))
            selected_field_list.append(selected_field)

        url = self.base_url + 'api/contacts/batch_update'
        params = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'field_choice': fields[3],
            'contact['+fields[3]+']':selected_field_list[2][2],
            'ids[]': contact_ids[0],
            'ids[]': contact_ids[1]
        }
        self.common.put_response_json(url, params, '批量编辑联系人')

    #快捷编辑联系人
    def quick_edit_contacts(self, contact_id):
        url = self.base_url + 'quick_edit/field_form?model=Contact&id=250705&field_name=name&page_type=index&_=1534228607097'
        params = {
            'model':'Contact',
            'id':contact_id,
            'field_name':'address.phone',
            'page_type':'index',
        }
        self.common.get_response_json(self, params, '快捷编辑联系人获取当前联系人的field name')

        url = self.base_url + 'api/contacts/' + str(contact_id)
        params = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'contact[id]': contact_id,
            'contact[name]': 'contact name'
        }

    #查重字段
    def check_duplicate_field(self, contact_id):
        url = self.base_url + 'api/contacts/check_duplicate_field.json'
        params = {
            'field':'tel',
            'field_value':'13512341234',
            'contact_id':contact_id
        }
        response = self.common.post_response_json(url, params, '查询电话是否重复')

    #写跟进
    def write_revisit_log(self, scope, contact_id):
        url = self.base_url + 'contacts/'+str(contact_id)+'/revisit_logs/new'
        params = {}
        self.common.get_response_json(url, params, '打开写跟进窗口')
        url = self.base_url + 'contacts/' +str(contact_id)+'/revisit_logs?contact_id='+str(contact_id)
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'revisit_log[category]':'89825',
            'revisit_log[real_revisit_at]':self.common.get_today_str_yymmddhhmm(),
            'revisit_log[content]':'写跟进%s' %self.common.get_random_int(999),
            'revisit_log[loggable_attributes][status]':'89822',
            'revisit_log[loggable_attributes][id]':str(contact_id),
            'revisit_log[remind_at]':''
        }
        self.common.post_response_json(url, params, '联系人列表页写跟进')


