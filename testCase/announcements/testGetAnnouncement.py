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


class GetAnnouncement:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.announcements_id = []
        self.params = ''
        pass

    # 根据需要这里获取到公告的list
    def get_announcements_list(self):
        url = self.base_url + 'announcements'
        # print(url)
        self.response = self.common.get_html(url, '获取公告列表')
        html_str = self.response.text
        soup = BeautifulSoup(html_str, "html.parser")
        self.announcements_id = re.findall(r'class="announcement-checkbox" type="checkbox" value="(.*?)"/>',
                                        str(soup))
        return self.announcements_id

    # 获取到公告管理的总条数
    def get_announcements_num(self):
        url = self.base_url + '/announcements'
        body = {}
        self.response = self.common.get_response_json(url, body, '获取公告列表')
        html_str = self.response.content
        soup = BeautifulSoup(html_str, "html.parser")
        total_num = re.findall(r"共 (.*?) 条", str(soup))
        n = int(total_num[0])
        return n
