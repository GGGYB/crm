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
from .testGetAnnouncement import GetAnnouncement

class UpdateAnnouncement:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.get_announcements = GetAnnouncement(cookie, csrf)
        self.announcements_id = []
        self.department_ids = []
        self.role_ids = []
        self.params = ''
        pass

    # 编辑公告信息
    def update_announcement(self):
        r = random.randint(1, self.get_announcements.get_announcements_num())
        self.announcements_id = self.get_announcements.get_announcements_list()
        rr = self.announcements_id[r-1]
        url = self.base_url + '/announcements/' + str(rr)
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'announcement[title]': 'for%sall'%self.common.get_random_int(99999),
            'announcement[visible_category]': 'all',
            'announcement[content]': '浦东西区%s号'%self.common.get_random_int(99999),
            ' commit': '发布'
        }
        response = self.common.post_response_xml(url,body, '编辑公告信息')
