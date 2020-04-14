# -*- coding: utf-8 -*-
__author__ = 'Jun'


from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.customers.testAddCustomer import AddCustomer
from testCase.departments.testGetDepartment import GetDepartment
from testCase.users import testGetUser as users

class GetContacts:
    def __init__(self, cookie, csrf):
        #'https://e.ikcrm.com/
        # self.base_url = base_url
        self.common = common.Common(cookie, csrf)
        self.testAddCustomer = AddCustomer(cookie, csrf)
        self.testGetDepartment = GetDepartment(cookie, csrf)
        self.user = users.GetUser(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.contacts_id =[]
        self.contacts_id1 = ''
        self.contact_id = ''
        self.contact_id =[]
        self.contact_id = ''
        pass


    #获得所有的我的联系人，我下属的联系人，我的联系人来查询
    def get_all_scope(self):
        url = self.base_url + 'contacts/'
        params = {
            'scope':'all_own',
            'section_only':'true'
        }
        response = self.common.get_response_json(url, params, '获取联系人页面的scope')
        soup = BeautifulSoup(response.content, 'html.parser')
        scopes = re.findall(r"contacts\?scope=(.*?)\">",str(soup))
        return scopes

    #联系人查重
    def duplicate_contacts(self):
        url = self.base_url + 'duplicate'
        params = {
            'add': 'yes',
            'key': 'contact'
        }
        self.common.get_response_json(url, params, '打开联系人查重')
        url = self.base_url + 'duplicate/search'
        params = {
            'key': 'contact',
            'query': '1351234'
        }
        response = self.common.get_response_json(url, params, '联系人查重')
        #To Be Done 查重没有数据之后新增联系人
        if response:
            print("Contact's duplication  is passed!")
        else:
            print("Sorry, Contact's duplication is fialed! ")

    # 获取当前页的contact_id
    def contact_ids(self):
        url = self.base_url + 'contact'
        body = {
            'order': 'asc',
            'scope': 'all_own',
            'sort': 'contacts.updated_at desc',
            'per_page': 10,
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, body, '获取当前页的联系人')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        # print S
        soup = BeautifulSoup(S, "html.parser")
        checked_contact = soup.find(attrs={'data-entity-table-name': 'Contact'})
        if checked_contact:
            a = str(checked_contact)
            contact_id_list = re.findall(r"data-id=\"(.*?)\">", a)
            return contact_id_list

    # 导出所选联系人
    def export_selected_contacts(self, scope):
        contact_ids = self.contact_ids()
        url = self.base_url + 'contacts?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope=' + scope + '&amp;sort=contacts.updated_at+desc&amp;type=advance&selected_ids%5B%5D=' + \
              contact_ids[0] + '&selected_ids%5B%5D=' + contact_ids[1] + '&format=js'
        self.common_get_resonse_json(url, 'export_selected_contacts')
        url = self.base_url + 'contacts.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope=' + scope + '&selected_ids%5B%5D=' + \
              contact_ids[0] + '&selected_ids%5B%5D=' + contact_ids[
                  1] + '&sort=contacts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export selected file')

    # 导出全部联系人
    def export_all_contacts(self, scope):
        url = self.base_url + 'contacts?format_type=calculate_export_pages&order=asc&per_page=10&scope=' + scope + '&sort=contacts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'export_all_contacts')

        # 点击下载文档
        url = self.base_url + 'contacts?export_page=1&format_type=xlsx&order=asc&per_page=10&scope=' + scope + '&sort=contacts.updated_at+desc&type=advance'
        self.common_get_resonse_json(url, 'excute download export all contact file')

    # 获取单个联系人详情
    def get_contact(self, contact_id):
        url = self.base_url + 'contacts/' + str(contact_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取当前用户详情')
        if response != False:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

    # 联系人写跟进
    def contacts_revisit_logs(self, soup, contact_id):
        status_list = re.findall(r"data-status=\"(.*?)\">", str(soup))
        if status_list:
            for status in status_list:
                url = self.base_url + 'api/contacts/%s/revisit_logs' % contact_id
                body = {
                    'utf8': '✓',
                    'authenticity_token': self.csrf,
                    'revisit_log[category]': '91160',
                    'revisit_log[real_revisit_at]': self.common.get_today_str_yymmddhhmm(),
                    'revisit_log[content]': '写跟进 wl-auto%s' % self.common.get_random_int(9999),
                    'revisit_log[loggable_attributes][status]': status,
                    'revisit_log[loggable_attributes][id]': contact_id,
                    'revisit_log[remind_at]': self.common.get_tomorrow_srt_yymmddhhmm()
                }
                response = self.common.post_response_json(url, body, '客户写跟进')
                if not response:
                    return {}

    # 查看联系人资料
    def get_contact_detail(self, contact_id):
        url = self.base_url + 'contacts/' + str(contact_id)
        params = {
            'only_base_info': 'true'
        }
        self.common.get_response_json(url, params, '获取客户的详细资料')

    # 查看相关联系人
    def get_contacts_belong_contact(self, customer_id,contact_id):
        url = self.base_url + 'api/contacts?page=&perPage=15&customer_id='+ str(customer_id)+'&contact_id='+ str(contact_id)
        params = {
            'page': '',
            'perPage': 15,
            'contact_id':contact_id,
            'contact_id': contact_id
        }
        self.common.get_response_json(url, params, '获取当前客户的联系人')

    # 查看联系人的商机
    def get_opportunities_belong_contact(self, contact_id):
        url = self.base_url + 'opportunities?page=&perPage=15&contact_id=' + str(contact_id)
        params = {
            'page': '',
            'perPage': 15,
            'contact_id': contact_id
        }
        self.common.get_response_json(url, params, '获取当前联系人的商机')


    # 查看联系人的操作日志
    def get_operation_logs(self, contact_id):
        url = self.base_url + 'api/operation_logs?page=&perPage=15&loggable_id='+ str(contact_id) +'&loggable_type=Contact'
        params = {
            'page': '',
            'perPage': 15,
            'loggable_id': contact_id,
            'loggable_type': 'Contact'
        }
        self.common.get_response_json(url, params, '查看客户的操作日志')



