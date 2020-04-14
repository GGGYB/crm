# -*- coding: utf-8 -*-

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

class Filters:
    def __init__(self, cookie, csrf):
        #'https://e.ikcrm.com/
        # self.base_url = base_url
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
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
        self.role_id = ''
       # 某些post或是get时要求header里带的信息，应该是一个帐户对应于唯一一个
        # 格式类似于：'Token token=cb5e0c1db161fe92a7f4ce67754821, uid=b9d28be2d18075de7435'
        pass
    """
    线索、数据（线索、客户、联系人）、联系人模块字段筛选查询
    """
    def filters_by_business(self, business_name, scopes):
        for scope in scopes:
            self.filters_by_scope(business_name, scope)

    def filters_by_scope(self, business_name, scope):
        url = self.base_url + business_name
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': business_name+'.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '业务模块是'+business_name)
        if not response:
                return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        template_ids = re.findall(r"data-template-id=\"(.*?)\"",str(soup))
        if template_ids:
            for template_id in template_ids:
                params['custom_field_template_id'] = template_id
                self.filters(soup, url, params, business_name)
        else:
            self.filters(soup, url, params, business_name)

   # 线索池模块字段筛选查询
    def lead_common_filters(self, lead_common_id):
        url = self.base_url + 'lead_commons'
        params = {
            'common_id': lead_common_id,
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '业务模块是' + 'lead_commons')
        if not response:
            return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        template_ids = re.findall(r"data-template-id=\"(.*?)\"",str(soup))
        if template_ids:
            for template_id in template_ids:
                params['custom_field_template_id'] = template_id
                self.filters(soup, url, params, 'lead_commons')
        else:
            self.lead_common_by_filters(soup, url, params, 'lead_commons',lead_common_id)


    ###线索、数据（线索、客户、联系人）、联系人查询 ###
    def filters(self, soup, url, params, business_name):
        self.filters_by_pinyin(soup, url, params, business_name)
        self.filters_by_custom_field(soup, url, params, business_name)
        self.filters_by_status(soup, url, params, business_name)
        self.filters_by_category(soup, url, params, business_name)
        self.filters_by_source(soup, url, params, business_name)
        self.filters_by_industry(soup, url, params, business_name)
        self.filters_by_staff_size(soup, url, params, business_name)
        self.filters_by_product(url, params, business_name)
        self.filters_by_real_visit_at(soup, url, params, business_name)
        self.filters_by_revisit_remind_at(soup, url, params, business_name)
        self.filters_by_created_at(soup, url, params, business_name)
        self.filters_by_updated_at(soup, url, params, business_name)
        self.filters_by_department(url, params, business_name)
        user_ids = self.users_get_all()
        self.filters_by_creater(url, params, user_ids, business_name)
        self.filters_by_assist_user(url, params, user_ids, business_name)
        self.filters_by_before_user(url, params, user_ids, business_name)
        self.filters_by_user(url, params, user_ids, business_name)
        self.filters_by_common_setting(url, params, business_name)
        # self.export(url, params)

    # 线索池
    def lead_common_by_filters(self, soup, url, params, business_name,lead_common_id):
        self.filters_by_custom_field(soup, url, params, business_name)
        self.filters_by_status(soup, url, params, business_name)
        self.filters_by_source(soup, url, params, business_name)
        self.lead_common_filters_by_real_visit_at(soup, url, params, business_name,lead_common_id)
        self.lead_common_filters_by_revisit_remind_at(soup, url, params, business_name,lead_common_id)
        self.lead_common_filters_by_created_at(soup, url, params, business_name,lead_common_id)
        self.lead_common_filters_by_updated_at(soup, url, params, business_name,lead_common_id)
        user_ids = self.users_get_all()
        self.filters_by_creater(url, params, user_ids, business_name)
        self.filters_by_before_user(url, params, user_ids, business_name)
        self.filters_by_latest_transfer_date(soup, url, params, business_name,lead_common_id)



    """
    #合同模块字段筛选查询
    """
    def contract_filters_by_business(self, business_name, scopes):
        for scope in scopes:
            self.contract_filters_by_scope(business_name, scope)

    def contract_filters_by_scope(self, business_name, scope):
        url = self.base_url + business_name
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': business_name + '.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '业务模块是' + business_name)
        if not response:
            return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        template_ids = re.findall(r"data-template-id=\"(.*?)\"", str(soup))
        if template_ids:
            for template_id in template_ids:
                params['custom_field_template_id'] = template_id
                self.contract_filters(soup, url, params, business_name)
        else:
            self.contract_filters(soup, url, params, business_name)

    #*****合同查询*****
    def contract_filters(self, soup, url, params, business_name):
        self.filters_by_custom_field(soup, url, params, business_name)
        self.filters_by_status(soup, url, params, business_name)
        self.filters_by_category(soup, url, params, business_name)
        self.filters_by_sign_date(soup, url, params, business_name)
        self.filters_by_start_at(soup, url, params, business_name)
        self.filters_by_end_at(soup, url, params, business_name)
        self.filters_by_real_visit_at(soup, url, params, business_name)
        self.filters_by_revisit_remind_at(soup, url, params, business_name)
        self.filters_by_created_at(soup, url, params, business_name)
        self.filters_by_updated_at(soup, url, params, business_name)
        self.filters_by_department(url, params, business_name)
        self.filters_by_payment_type(soup, url, params, business_name)
        user_ids = self.users_get_all()
        self.filters_by_creater(url, params, user_ids, business_name)
        self.filters_by_assist_user(url, params, user_ids, business_name)
        self.filters_by_before_user(url, params, user_ids, business_name)
        self.filters_by_user(url, params, user_ids, business_name)
        self.filters_by_receive_user(url, params, user_ids, business_name)

    """"
    回款模块字段筛选查询
    """
    def receive_payments_filters_by_business(self, business_name, scopes):
        for scope in scopes:
            self.filters_by_scope(business_name, scope)

    def receive_payments_filters_by_scope(self, business_name, scope):
        url = self.base_url + business_name
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': business_name + '.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '业务模块是' + business_name)
        if not response:
            return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        template_ids = re.findall(r"data-template-id=\"(.*?)\"", str(soup))
        if template_ids:
            for template_id in template_ids:
                params['custom_field_template_id'] = template_id
                self.receive_payments_filters(soup, url, params, business_name)
        else:
            self.receive_payments_filters(soup, url, params, business_name)

    #******回款查询*****
    def receive_payments_filters(self, soup, url, params, business_name):
        self.departments_get_all()
        self.filters_by_contract_department(url, params, business_name)
        user_ids = self.users_get_all()
        self.filters_by_contract_user(url, params, business_name)
        self.filters_by_receive_payment_status(soup, url, params, business_name)
        self.filters_by_contract_name(url, params, business_name)
        self.filters_by_receive_plans_date(soup, url, params, business_name)
        self.filters_by_overdue_status(soup, url, params, business_name)
        self.filters_by_received_types(soup, url, params, business_name)
        self.filters_by_receive_user(soup, url, params, business_name)
        self.filters_by_receive_date(soup, url, params, business_name)
        self.filters_by_payment_type(soup, url, params, business_name)
        self.filters_by_invoiced_date(soup, url, params, business_name)
        self.filters_by_invoice_types(soup, url, params, business_name)
        self.filters_by_broker_user(soup, url, params, business_name)
        self.filters_by_user(url, params, user_ids, business_name)

    """"
    费用报销模块字段筛选查询
    """
    def expense_center_filters_by_business(self, business_name, scopes):
        for scope in scopes:
            self.filters_by_scope(business_name, scope)

    def expense_center_filters_by_scope(self, business_name, scope):
        url = self.base_url + business_name
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': business_name + '.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '业务模块是' + business_name)
        if not response:
            return {}
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        template_ids = re.findall(r"data-template-id=\"(.*?)\"", str(soup))
        if template_ids:
            for template_id in template_ids:
                params['custom_field_template_id'] = template_id
                self.expense_center_filters(soup, url, params, business_name)
        else:
            self.expense_center_filters(soup, url, params, business_name)

    #*****费用报销*****
    def expense_center_filters(self, soup, url, params, business_name):
        self.departments_get_all()
        self.filters_by_department(url, params, business_name)
        user_ids = self.users_get_all()
        self.filters_by_expenses_category(soup, url, params, business_name)


    #获取当前企业用户的user_id
    def get_user_id(self,role_id):
        url = self.base_url + 'user_center/users'
        #https://e.ikcrm.com/user_center/users
        print (url)
        body = {
            'utf8':'✓',
            'authenticity_token': self.csrf,
            'user[id]':'',
            'user[name]':'tester%s'%self.common.get_random_int(9999),
            'user[gender]':'male',
            'user[phone]':'1971234%s'%self.common.get_random_int(9999),
            'user[email]':'1971234%s@qq.com' %self.common.get_random_int(9999),
            'user[roles_user_attributes][role_id]':role_id,
            'user[superior_id]':'',
            'user[users_department_attributes][id]':'',
            'user[users_department_attributes][department_id]':'',
        }
        response = self.common.get_response_json(url, body, '获取当前用户')
        if not response:
            return {}
        print (self.response.json()['data']['id'])
        return self.response.json()['data']['id']


    #根据自定义字段查询数据（线索、客户、联系人）
    def filters_by_custom_field(self, soup, url, params, business_name):
        checked_custom_field = soup.find(attrs={'id':'custom_field_name'})
        if checked_custom_field:
            custom_field_list = re.findall(r"value=\"(.*?)\">",str(checked_custom_field))
        for custom_field in custom_field_list:
            params.setdefault('custom_field_name', custom_field)
            params.setdefault('search_key', '13023195853')
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + '按照自定义搜索:  自定义内容是 : '+ custom_field)
    #根据首字母查询数据（线索、客户、联系人）
    def filters_by_pinyin(self, soup, url, params, business_name):
        checked_pinyin = soup.find(attrs={'data-name':'name_pinyin'})
        if checked_pinyin:
            pinyin_content = checked_pinyin.find(attrs={'class':'auto'})
            pinyin_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(pinyin_content))
            for first_letter in pinyin_list:
                if first_letter == '%23':
                    params['filters[][operator]'] = 'non_start_with'
                    params['filters[][query]'] = '#'
                else:
                    params['filters[][operator]'] = 'start_with'
                    params['filters[][query]'] = first_letter
                params['filters[][name]'] = 'name_pinyin'
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据首字母查询')
    #根据数据（线索、线索池，客户、联系人）状态查询数据
    def filters_by_status(self, soup, url, params, business_name):
        checked_status = soup.find(attrs={'data-name':'status'})
        if checked_status:
            status_content = checked_status.find(attrs={'class':'auto'})
            status_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(status_content))
            for status in status_list:
                params = self.update_params(params, 'status', 'equal', status)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据状态查询: '+ status)
    #数据（线索、客户、联系人）类型
    def filters_by_category(self, soup, url, params, business_name):
        checked_category = soup.find(attrs={'data-name':'category'})
        if checked_category:
            category_content = checked_category.find(attrs={'class':'auto'})
            category_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(category_content))
            for category in category_list:
                params = self.update_params(params, 'category', 'equal', category)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据数据（线索、客户、联系人）类型查询')
    #数据（线索、线索池，客户、联系人）来源
    def filters_by_source(self, soup, url, params, business_name):
        checked_source = soup.find(attrs={'data-name':'source'})
        if checked_source:
            source_content = checked_source.find(attrs={'class':'auto'})
            source_content = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(source_content))
            for source in source_content:
                params = self.update_params(params, 'source', 'equal', source)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据数据（线索、客户、联系人）来源查询')
    #所属行业
    def filters_by_industry(self, soup, url, params, business_name):
        checked_industry = soup.find(attrs={'data-name':'industry'})
        if checked_industry:
            industry_content = checked_industry.find(attrs={'class':'auto'})
            a = str(industry_content)
            industry_content = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            for industry in industry_content:
                params = self.update_params(params, 'industry', 'equal', industry)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据所属行业查询')
    #人员规模
    def filters_by_staff_size(self, soup, url, params, business_name):
        checked_staff_size = soup.find(attrs={'data-name':'staff_size'})
        if checked_staff_size:
            staff_size_content = soup.find(attrs={'data-name':'staff_size'}).find(attrs={'class':'auto'})
            a = str(staff_size_content)
            staff_size_content = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            for staff_size in staff_size_content:
                params = self.update_params(params, 'staff_size', 'equal', staff_size)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 按照人员规模查询')
    #已成交产品
    def filters_by_product(self, url, params, business_name):
        product_ids = self.products_get_all()
        for product_id in product_ids:
            params['product_id'] = product_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据已成交产品来查询')
    #根据实际跟进时间（线索、客户、联系人）
    def filters_by_real_visit_at(self, soup, url, params, business_name):
        checked_real_revisit_at = soup.find(attrs={'data-name':'real_revisit_at'})
        if checked_real_revisit_at:
            real_revisit_at_content = checked_real_revisit_at.find(attrs={'class':'wrapper-link'})
            real_revisit_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(real_revisit_at_content))
            real_revisit_at_list.append('custom_time')
            for real_revisit_at in real_revisit_at_list:
                if real_revisit_at == 'custom_time':
                    url = url + '?filters[][name]=real_revisit_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort='+business_name+'.updated_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'real_revisit_at', 'within', real_revisit_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据实际跟进时间')
    # 根据实际跟进时间（线索池）
    def lead_common_filters_by_real_visit_at(self, soup, url, params, business_name,lead_common_id):
        checked_real_revisit_at = soup.find(attrs={'data-name': 'real_revisit_at'})
        if checked_real_revisit_at:
            real_revisit_at_content = checked_real_revisit_at.find(attrs={'class': 'wrapper-link'})
            real_revisit_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",
                                              str(real_revisit_at_content))
            real_revisit_at_list.append('custom_time')
            for real_revisit_at in real_revisit_at_list:
                if real_revisit_at == 'custom_time':
                    url = url + '?common_id= '+ str(lead_common_id) +'&filters[][name]=real_revisit_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort=lead_extra.flow_into_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'real_revisit_at', 'within', real_revisit_at)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据实际跟进时间')

    #根据下次跟进时间查询数据（线索、客户、联系人）
    def filters_by_revisit_remind_at(self, soup, url, params, business_name):
        checked_revisit_remind_at = soup.find(attrs={'data-name':'revisit_remind_at'})
        if checked_revisit_remind_at:
            revisit_remind_at_content = checked_revisit_remind_at.find(attrs={'class':'wrapper-link'})
            revisit_remind_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(revisit_remind_at_content))
            revisit_remind_at_list.append('custom_time')
            for revisit_remind_at in revisit_remind_at_list:
                if revisit_remind_at == 'custom_time':
                    url = url + '?filters[][name]=revisit_remind_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort='+business_name+'.updated_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'revisit_remind_at', 'within', revisit_remind_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据下次跟进时间')

     # 根据下次跟进时间查询数据（线索池）
    def lead_common_filters_by_revisit_remind_at(self, soup, url, params, business_name,lead_common_id):
         checked_revisit_remind_at = soup.find(attrs={'data-name': 'revisit_remind_at'})
         if checked_revisit_remind_at:
             revisit_remind_at_content = checked_revisit_remind_at.find(attrs={'class': 'wrapper-link'})
             revisit_remind_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",
                                                 str(revisit_remind_at_content))
             revisit_remind_at_list.append('custom_time')
             for revisit_remind_at in revisit_remind_at_list:
                 if revisit_remind_at == 'custom_time':
                     url = url +  '?common_id= '+ str(lead_common_id) +'&filters[][name]=revisit_remind_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort=lead_extra.flow_into_at%20desc&type=advance&per_page=50'
                     params = {}
                 else:
                     params = self.update_params(params, 'revisit_remind_at', 'within', revisit_remind_at)
                 self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据下次跟进时间')
    #根据创建时间选择数据（线索、客户、联系人）
    def filters_by_created_at(self, soup, url, params, business_name):
        checked_created_at = soup.find(attrs={'data-name':'created_at'})
        if checked_created_at:
            create_at_content = checked_created_at.find(attrs={'class':'wrapper-link'})
            a = str(create_at_content)
            create_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            create_at_list.append('custom_time')
            for create_at in create_at_list:
                if create_at == 'custom_time':
                    url = url + '?filters[][name]=create_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort='+business_name+'.updated_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'create_at', 'within', create_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据创建时间修改')

     # 根据创建时间选择数据（线索池）
    def lead_common_filters_by_created_at(self, soup, url, params, business_name,lead_common_id):
        checked_created_at = soup.find(attrs={'data-name': 'created_at'})
        if checked_created_at:
            create_at_content = checked_created_at.find(attrs={'class': 'wrapper-link'})
            a = str(create_at_content)
            create_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", a)
            create_at_list.append('custom_time')
            for create_at in create_at_list:
                if create_at == 'custom_time':
                    url = url + '?common_id= '+ str(lead_common_id) +'&filters[][name]=create_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort=lead_extra.flow_into_at+%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'create_at', 'within', create_at)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据创建时间修改')

    #根据更新于时间选择数据（线索、客户、联系人）
    def filters_by_updated_at(self, soup, url, params, business_name):
        checked_updated_at = soup.find(attrs={'data-name':'updated_at'})
        if checked_updated_at:
            updated_at_content = checked_updated_at.find(attrs={'class':'wrapper-link'})
            a = str(updated_at_content)
            update_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            update_at_list.append('custom_time')
            for update_at in update_at_list:
                if update_at == 'custom_time':
                    url = url + '?filters[][name]=update_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort='+business_name+'.updated_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'update_at', 'within', update_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据更新于时间选择')

            # 根据更新于时间选择数据（线索池）
    def lead_common_filters_by_updated_at(self, soup, url, params, business_name,lead_common_id):
        checked_updated_at = soup.find(attrs={'data-name': 'updated_at'})
        if checked_updated_at:
            updated_at_content = checked_updated_at.find(attrs={'class': 'wrapper-link'})
            a = str(updated_at_content)
            update_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", a)
            update_at_list.append('custom_time')
            for update_at in update_at_list:
                if update_at == 'custom_time':
                    url = url + '?common_id= '+ str(lead_common_id) +'&filters[][name]=update_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort=lead_extra.flow_into_at%20desc&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'update_at', 'within', update_at)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据更新于时间选择')
    #根据所属部门来获取全部数据（线索、客户、联系人）
    def filters_by_department(self, url, params, business_name):
        department_ids = self.departments_get_all()
        for department_id in department_ids:
            params['department_id'] = department_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据所选部门查询')
    #根据创建人/协作人/前负责人/负责人 来获取全部数据（线索、客户、联系人）
    def filters_by_creater(self, url, params, user_ids, business_name):
        for user_id in user_ids:
            params['creator_id'] = user_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + '根据创建人查询')
    #根据协作人来获取
    def filters_by_assist_user(self, url, params, user_ids, business_name):
        for user_id in user_ids:
            params['assist_user_id'] = user_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据协作人来查询')
    #根据前负责人来查询
    def filters_by_before_user(self, url, params, user_ids, business_name):
        for user_id in user_ids:
            params['before_user_id'] = user_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据前负责人来查询')
    #根据负责人来查询
    def filters_by_user(self, url, params, user_ids, business_name):
        for user_id in user_ids:
            params['user_id'] = user_id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据负责人来查询')
    #根据所属公海来查询
    def filters_by_common_setting(self, url, params, business_name):
        common_setting_ids = self.common_settings_get_all()
        for id in common_setting_ids:
            params['before_customer_common_setting_id'] = id
            self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据所属公海查询')
     # 根据最新转入时间来查询（线索池）
    def  filters_by_latest_transfer_date(self, soup, url, params, business_name,lead_common_id):
        checked_real_revisit_at = soup.find(attrs={'data-name':'lead_extra.flow_into_at'})
        if checked_real_revisit_at:
            flow_into_at_content = checked_real_revisit_at.find(attrs={'class':'wrapper-link'})
            flow_into_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",str(flow_into_at_content))
            flow_into_at_list.append('custom_time')
            for flow_into_at in flow_into_at_list:
                if flow_into_at == 'custom_time':
                    url = url + '?common_id= '+ str(lead_common_id) +'&filters[][name]=lead_extra.flow_into_at&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&type=advance&per_page=50'
                    params = {}
                else:
                    params = self.update_params(params, 'lead_extra.flow_into_at', 'within', flow_into_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 最新转入时间来查询')

    def update_params(self, params, filter_name, operator, filter_query):
        params['filters[][name]'] = filter_name
        params['filters[][operator]'] = operator
        params['filters[][query]'] = filter_query
        return params

    #获取产品ID
    def products_get_all(self):
        url = self.base_url + 'api/products'
        params = {
            'page':'',
            'perPage':'',
            'from_sold_customer':'true',
            'term':'',
            'page':'1',
            'perPage':'15'
        }
        response = self.common.get_response_json(url, params, '获取产品id')
        if not response:
            return {}
        product_models = response.json()['models']
        product_ids = []
        if response.json()['total_count'] != 0:
            for product in product_models:
                product_ids.append(product['id'])
        return product_ids

    #获取所有的部门
    def departments_get_all(self):
        url = self.base_url + 'api/departments'
        params = {
            'name':'',
            'page':'1',
            'perPage':'15'
        }
        response = self.common.get_response_json(url, params, '获取所有的部门')
        if not response:
            return {}
        department_models = response.json()['models']
        department_ids = []
        for department in department_models:
            department_ids.append(department['id'])
        return department_ids

    #获取所有的用户id
    def users_get_all(self):
        url = self.base_url + 'api/users'
        params = {
            'username': '',
            'page': 1,
            'perPage': 15
        }
        response = self.common.get_response_json(url, params, '获取用户')
        if not response:
            return {}
        user_models = response.json()['models']
        user_ids = []
        for user in user_models:
            user_ids.append(user['id'])
        return user_ids

    #获取所有公海
    def common_settings_get_all(self):
        url = self.base_url + 'api/customer_common_settings'
        params = {
            'name': '',
            'page': 1,
            'perPage': 15
        }
        response = self.common.get_response_json(url, params, '获取所有的公海')
        if not response:
            return {}
        common_settings = response.json()['models']
        common_setting_ids = []
        for common_setting in common_settings:
            common_setting_ids.append(common_setting['id'])
        return common_setting_ids

    """
    合同模块筛选条件的字段：签约日期、合同开始日期、合同结束日期
    """
    #根据签约日期选择合同
    def filters_by_sign_date(self, soup, url, params, business_name):
        checked_sign_date = soup.find(attrs={'data-name':'sign_date'})
        if checked_sign_date:
            sign_date_content = checked_sign_date.find(attrs={'class':'wrapper-link'})
            a = str(sign_date_content)
            sign_date_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            sign_date_list.append('custom_time')
            for sign_date in sign_date_list:
                if sign_date == 'custom_time':
                    url = url + '?filters[][name]=sign_date&filters[][operator]=within&filters[][query][]=2018-02-09&filters[][query][]=2018-03-08&sort='+business_name+'.updated_at%20desc&type=advance&per_page=50&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'create_at', 'within', sign_date)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据签约日期查询合同')

    # 根据合同开始时间选择合同
    def filters_by_start_at(self, soup, url, params, business_name):
        checked_start_at = soup.find(attrs={'data-name':'start_at'})
        if checked_start_at:
            start_at_content = checked_start_at.find(attrs={'class':'wrapper-link'})
            a = str(start_at_content)
            start_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            start_at_list.append('custom_time')
            for start_at in start_at_list:
                if start_at == 'custom_time':
                    url = url + '?scope=all_own&type=advance&per_page=50filters[][name]=start_at&filters[][operator]=within&filters[][query][]=2018-07-09&filters[][query][]=2018-08-28&sort='+business_name+'.updated_at%20desc&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'create_at', 'within', start_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据合同开始时间查询合同')
    # 根据合同结束时间选择合同
    def filters_by_end_at(self, soup, url, params, business_name):
        checked_end_at = soup.find(attrs={'data-name':'end_at'})
        if checked_end_at:
            end_at_content = checked_end_at.find(attrs={'class':'wrapper-link'})
            a = str(end_at_content)
            end_at_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;",a)
            end_at_list.append('custom_time')
            for end_at in end_at_list:
                if end_at == 'custom_time':
                    url = url + '?scope=all_own&type=advance&per_page=50filters[][name]=start_at&filters[][operator]=within&filters[][query][]=2018-07-09&filters[][query][]=2018-08-28&sort='+business_name+'.updated_at%20desc&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'create_at', 'within', end_at)
                self.common.get_response_json(url, params, '业务模块是：'+ business_name + ' 根据合同结束时间查询合同')

    """
    回款模块筛选条件字段：
    """
    # 根据回款状态筛选status
    def filters_by_receive_payment_status(self, soup, url, params, business_name):
        checked_status = soup.find(attrs={'data-name': 'status'})
        if checked_status:
            status_content = checked_status.find(attrs={'class': 'auto'})
            status_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(status_content))
            for status in status_list:
                params = self.update_params(params, 'status', 'equal', status)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据状态查询: ' + status)

    # 根据合同所属部门筛选
    def filters_by_contract_department(self, url, params, business_name):
        department_ids = self.departments_get_all()
        for department_id in department_ids:
            params['department_id'] = department_id
            self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据合同所选部门查询')

    # 跟进合同负责人筛选
    def filters_by_contract_user(self, url, params, user_ids, business_name):
        for user_id in user_ids:
            params['user_id'] = user_id
            self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据合同负责人来查询')

    # 获取所有合同
    def contracts_get_all(self):
        url = self.base_url + 'contracts'
        params = {
            'name': '',
            'page': '1',
            'perPage': '15'
        }
        response = self.common.get_response_json(url, params, '获取所有的合同')
        if not response:
            return {}
        contract_models = response.json()['models']
        contract_ids = []
        for contract in contract_models:
            contract_ids.append(contract['id'])
        return contract_ids

    # 根据合同标题
    def filters_by_contract_name(self, url, params, business_name):
        contract_ids = self.contracts_get_all()
        for contract_id in contract_ids:
            params['contract_id'] = contract_id
            self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据合同所选部门标题查询')

    # 根据计划回款日期
    def filters_by_receive_plans_date(self, soup, url, params, business_name):
        checked_receive_date = soup.find(attrs={'data-name': 'receive_date'})
        if checked_receive_date:
            receive_date_content = checked_receive_date.find(attrs={'class': 'wrapper-link'})
            receive_date_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(receive_date_content))
            receive_date_list.append('custom_time')
            for receive_date in receive_date_list:
                if receive_date == 'custom_time':
                    url = url + 'received_payment_center/received_payment_plans?filters[][name]=receive_date&filters[][operator]=within&filters[][query][]=2018-08-02&filters[][query][]=2018-08-08&scope=received_payment_plans&type=advance&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'receive_date', 'within', receive_date)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据计划回款日期查询')

    # 根据逾期状态
    def filters_by_overdue_status(self, soup, url, params, business_name):
        checked_overdue_status = soup.find(attrs={'data-name': 'overdue_status'})
        if checked_overdue_status:
            overdue_status_content = checked_overdue_status.find(attrs={'class': 'auto'})
            overdue_status_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(overdue_status_content))
            for overdue_status in overdue_status_list:
                params = self.update_params(params, 'overdue_status', 'equal', overdue_status)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据逾期状态查询: ' + overdue_status)

    # 根据回款类型
    def filters_by_received_types(self, soup, url, params, business_name):
        checked_received_types = soup.find(attrs={'data-name': 'received_types'})
        if checked_received_types:
            received_types_content = checked_received_types.find(attrs={'class': 'auto'})
            received_types_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(received_types_content))
            for received_types in received_types_list:
                params = self.update_params(params, 'received_types', 'equal', received_types)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据回款类型查询')

    # 根据收款人
    def filters_by_receive_user(self, url, params, user_ids, business_name):
        for receive_user_id in user_ids:
            params['receive_user_id'] = receive_user_id
            self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据收款人来查询')

    # 根据回款日期
    def filters_by_receive_date(self, soup, url, params, business_name):
        checked_receive_date = soup.find(attrs={'data-name': 'receive_date'})
        if checked_receive_date:
            receive_date_content = checked_receive_date.find(attrs={'class': 'wrapper-link'})
            receive_date_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(receive_date_content))
            receive_date_list.append('custom_time')
            for receive_date in receive_date_list:
                if receive_date == 'custom_time':
                    url = url + 'received_payment_center/received_payments?filters[][name]=receive_date&filters[][operator]=within&filters[][query][]=2018-08-02&filters[][query][]=2018-08-08&&scope=received_payments&type=advance&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'receive_date', 'within', receive_date)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据回款日期查询')

    # 根据付款方式
    def filters_by_payment_type(self, soup, url, params, business_name):
        checked_payment_type = soup.find(attrs={'data-name': 'payment_type'})
        if checked_payment_type:
            payment_type_content = checked_payment_type.find(attrs={'class': 'auto'})
            payment_type_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(payment_type_content))
            for payment_type in payment_type_list:
                params = self.update_params(params, 'payment_type', 'equal', payment_type)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据付款方式查询')

    # 根据开票日期
    def filters_by_invoiced_date(self, soup, url, params, business_name):
        checked_invoiced_date = soup.find(attrs={'data-name': 'invoiced_date'})
        if checked_invoiced_date:
            invoiced_date_content = checked_invoiced_date.find(attrs={'class': 'wrapper-link'})
            invoiced_date_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(invoiced_date_content))
            invoiced_date_list.append('custom_time')
            for invoiced_date in invoiced_date_list:
                if invoiced_date == 'custom_time':
                    url = url + 'received_payment_center/invoiced_payments?filters[][name]=receive_date&filters[][operator]=within&filters[][query][]=2018-08-02&filters[][query][]=2018-08-08&scope=invoiced_payments&type=advance&section_only=true'
                    params = {}
                else:
                    params = self.update_params(params, 'invoiced_date', 'within', invoiced_date)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据开票日期查询')

    # 根据票据类型
    def filters_by_invoice_types(self, soup, url, params, business_name):
        checked_invoice_types = soup.find(attrs={'data-name': 'invoice_types'})
        if checked_invoice_types:
            invoice_types_content = checked_invoice_types.find(attrs={'class': 'auto'})
            invoice_types_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(invoice_types_content))
            for invoice_types in invoice_types_list:
                params = self.update_params(params, 'invoice_types', 'equal', invoice_types)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据票据类型查询')

    # 根据经手人
    def filters_by_broker_user(self, url, params, user_ids, business_name):
        for broker_user_id in user_ids:
            params['broker_user_id'] = broker_user_id
            self.common.get_response_json(url, params, '业务模块是：' + business_name + ' 根据收款人来查询')

    # 导出所有
    def export(self, url, params):
        params['format_type'] = 'calculate_export_pages'
        self.common.get_response_json(url, params, '导出所有的')

        params['format_type'] = 'xlsx'
        self.common.get_response_json(url, params, '下载导出所有的excel')

    # 导出所选的
    def export_selected(self, business_name, id_list):
        url = self.base_url + business_name
        params = {
            'export_page': '1',
            'amp;format_type': 'calculate_export_pages',
            'amp;order': 'asc',
            'amp;per_page': '50',
            'amp;scope': 'all_own',
            'amp;sort': 'customers.updated_at desc',
            'amp;type': 'advance',
            'selected_ids[]': id_list[0],
            'selected_ids[]': id_list[1],
            'format': 'js'
        }

    """
    费用报销模块筛选条件字段：
    """
    def filters_by_expenses_category(self, soup, url, params, business_name):
        checked_expenses_category = soup.find(attrs={'data-name': 'received_types'})
        if checked_expenses_category:
            expenses_category_content = checked_expenses_category.find(attrs={'class': 'auto'})
            expenses_category_list = re.findall(r"filters%5B%5D%5Bquery%5D=(.*?)&amp;", str(expenses_category_content))
            for expenses_category in expenses_category_list:
                params = self.update_params(params, 'expenses_category', 'equal', expenses_category)
                self.common.get_response_json(url, params, '业务模块是：' + business_name + '根据费用类型查询')