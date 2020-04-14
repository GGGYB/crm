from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
import copy
from decimal import Decimal as D
from commons import common
from commons.const import const


class UpdateOrganization:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.announcements_id = []
        self.staff_size_list = []
        self.organization_industry = []
        self.organization_id = []
        self.params = ''
        pass

    # 获取公司规模list和所属行业list
    def get_staff_size(self):
        url = self.base_url + '/user_center/organization/edit'
        response = self.common.get_html(url, '获取公司信息的页面')
        soup = BeautifulSoup(response.text, 'html.parser')
        staff_size = soup.findAll(attrs={'id': 'organization_client_attributes_staff_size'})
        self.staff_size_list = re.findall(r"value=\"(.*?)\">", str(staff_size))
        organization_industry = soup.findAll(attrs={'id': 'organization_client_attributes_industry'})
        self.organization_industry = re.findall(r"value=\"(.*?)\">", str(organization_industry))
        id = soup.findAll(attrs={"id": "organization_client_attributes_id"})
        self.organization_id = re.findall(r'value=\"(.*?)"', str(id))
        i = self.common.get_random_int(len(self.staff_size_list)-1)
        n = self.common.get_random_int(len(self.organization_industry)-1)
        return self.staff_size_list[i],self.organization_industry[n],self.organization_id[0]

    # 编辑公司信息
    def update_organization(self):
        url = self.base_url + '/user_center/organization'
        staff_size = self.get_staff_size()[0]
        organization_industry = self.get_staff_size()[1]
        organization_id = self.get_staff_size()[2]
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'attachment_id': '',
            'organization[client_attributes][shorter_name]':'234465',
            'organization[client_attributes][industry]':organization_industry,
            'organization[client_attributes][province_id]': '9',
            'organization[client_attributes][city_id]': '73',
            'organization[client_attributes][district_id]': '732',
            'organization[client_attributes][address_detail]': '1232',
            'organization[client_attributes][staff_size]':staff_size,
            'organization[client_attributes][id]':organization_id,
        }
        self.response = self.common.post_response_json(url, body, '编辑了公司信息')






