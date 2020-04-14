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
from testCase.departments import testGetDepartment as departments
from .testGetAnnouncement import GetAnnouncement

class AddAnnouncement:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.get_announcements = GetAnnouncement(cookie, csrf)
        self.departments = departments.GetDepartment(cookie, csrf)
        self.announcements_id = []
        self.department_ids = []
        self.role_ids = []
        self.params = ''
        pass

    # 新增公告，可见范围是全公司
    def add_announcements_all(self):
        url = self.base_url + 'announcements'
        n = self.get_announcements.get_announcements_num() + 1
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'announcement[title]': 'forall',
            'announcement[visible_category]': 'all',
            'announcement[content]': ' 新增公告_可见范围是%s全公司'%self.common.get_random_int(9999999),
            ' commit': '发布'
        }
        response = self.common.post_response_xml(url, body, '新增公告，可见范围是全公司')
        s = self.get_announcements.get_announcements_num()
        success = self.common.check_data(s, n, "新增公告_可见范围是全公司")


    # 新增公告，可见范围是任意部门
    def add_announcements_department(self):
        end = random.randint(1, len(self.departments.getDepartmentId()))
        n = self.get_announcements.get_announcements_num() + 1
        b = []
        for i in range(end):
            start = self.common.get_random_int(len(self.departments.getDepartmentId()))
            b.append(self.departments.getDepartmentId()[start])
            b = list(set(b))
        for i in range(len(b)):
            url = self.base_url + 'announcements'
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'announcement[title]': 'fordepartment',
                'announcement[visible_category]': 'departments',
                'announcement[visible_ids][]': b,
                'announcement[content]': '新增公告_可见范围是%s任意部门'%self.common.get_random_int(9999999),
                ' commit': '发布'
            }
        response = self.common.post_response_xml(url, body, '新增公告,可见范围是任意部门')
        s = self.get_announcements.get_announcements_num()
        success = self.common.check_data(s, n, "新增公告_可见范围是任意部门")


    # 获取角色list
    def get_role_list(self):
        url = self.base_url + '/announcements/new'
        response = self.common.get_html(url, '获取公司信息的页面')
        soup = BeautifulSoup(response.text, 'html.parser')
        role_list = soup.findAll(attrs={'id': 'radioDiv2'})
        self.role_ids = re.findall(r"value=\"(.*?)\">", str(role_list))
        return self.role_ids

    # 新增公告，可见范围是任意角色
    def add_announcements_role(self):
        end = random.randint(1, len(self.get_role_list()))
        n = self.get_announcements.get_announcements_num() + 1
        b = []
        for i in range(end):
            start = self.common.get_random_int(len(self.get_role_list()))
            b.append(self.role_ids[start])
            b = list(set(b))
        for i in range(len(b)):
            url = self.base_url + 'announcements'
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'announcement[title]': 'forroles',
                'announcement[visible_category]': 'roles',
                'announcement[visible_ids][]': b,
                'announcement[content]': '新增公告_可见范围是%s任意角色'%self.common.get_random_int(9999999),
                ' commit': '发布'
            }
        response = self.common.post_response_xml(url, body, '新增公告可见范围是任意角色')
        s = self.get_announcements.get_announcements_num()
        success = self.common.check_data(s, n, "新增公告_可见范围是任意角色")





