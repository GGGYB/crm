# -*- coding: utf-8 -*-
__author__ = 'Jun'


from commons import common
from commons.const import const
from testCase.customers.testAddCustomer import AddCustomer
from testCase.departments.testGetDepartment import GetDepartment
from testCase.users import testGetUser as users

class AddContact:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.customers_id =[]
        self.params = ''
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.testGetDepartment = GetDepartment(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        pass

    #新增联系人
    def add_contact(self):
        url = self.base_url + 'api/contacts'
        body = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'refer_call_record_id':'',
            'contact[id]':'',
            'contact[name]':'联系人%s' %self.common.get_today_str_yymmddhhmm(),
            'contact[customer_id]':  self.testAddCustomer.add_customers(),
            'contact[department]':'',
            'contact[job]':'',
            'contact[address_attributes][tel]':'191%s' %self.common.get_random_int(99999999),
            'contact[address_attributes][phone]':'',
            'contact[address_attributes][wechat]':'',
            'contact[address_attributes][qq]':'',
            'contact[address_attributes][wangwang]':'',
            'contact[address_attributes][email]':'test%s @test.com' %self.common.get_random_int(9999),
            'contact[address_attributes][url]':'www.test%s.com' %self.common.get_random_int(9999),
            'china_tag_id':'4',
            'contact[address_attributes][country_id]':'4',
            'contact[address_attributes][province_id]':'',
            'contact[address_attributes][city_id]':'',
            'contact[address_attributes][district_id]':'',
            'contact[address_attributes][detail_address]':'',
            'contact[address_attributes][zip]':'',
            'contact[gender]':'',
            'contact[birth_date]':'',
            'contact[note]': '123',
            # 'contact[user_id]': self.user.getMyUserId(),
            # 'contact[want_department_id]':self.DepartmentId.getDepartmentId()
        }
        response = self.common.post_response_json(url, body, '新增联系人是'+url)
        if not response:
            return {}
        self.response = response
        contact_id = self.response.json()['data']['id']
        return contact_id

    #扫描名片
    def contacts_camcard_launch(self):
        url = self.base_url + 'contacts/camcard_launch'
        body = {}
        self.common.get_response_json(url, body, '打开扫描名片窗口')
        #开始扫描
        url = self.base_url + 'contacts/camcard_explain'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'attachment_id':'33272'
        }
        self.common.post_response_json(url, params, '联系人-扫描名片添加图片')
        #开始添加联系人
        url = self.base_url + 'api/contacts/camcard'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'attachment_id':'33276',
            'entity_attributes[name]':'联系人名称%s' %self.common.get_random_int(99999999),
            'entity_attributes[company_name]':'扫描名片添加联系人%s' %self.common.get_random_int(99999999),
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
        self.common.post_response_json(url, params, '扫描名片添加联系人')

    #新增任务
    def add__event_for_contact(self, contact_id):
        url = self.base_url + 'events/new?ajax_back_to=%2Fevents%3Fentity_id%3D111662%26entity_klass%3DContact&entity_id='+str(contact_id)+'&entity_klass=Contact'
        params = {}
        self.common.get_response_json(url, params, '联系人详情页新增任务打开窗口')
        url = self.base_url + 'api/events'
        params = {
            'utf8':'✓',
            'authenticity_token':self.csrf,
            'event[note]':'打电话给客户',
            'event[remind_at]': self.common.get_today_str_yymmddhhmm(),
            'event[remind_type]':'punctual',
            'event[related_item_id]':str(contact_id),
            'event[related_item_type]':'Contact',
            'event[user_ids]': str(self.user.getMyUserId())
        }
        response = self.common.post_response_json(url, params, '给单个联系人新增任务')
        id = response.json()['data']['id']
