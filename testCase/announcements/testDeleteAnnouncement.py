from bs4 import BeautifulSoup
import json
import requests
import random
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from .testGetAnnouncement import GetAnnouncement


class DeleteAnnouncement:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.get_announcements = GetAnnouncement(cookie, csrf)
        self.announcements_id = []
        self.params = ''
        pass

   # 批量删除公告，随机删除随机条数
    def batch_delete_announcements(self):
        url = self.base_url + 'announcements/bulk_delete'
        self.announcements_id = self.get_announcements.get_announcements_list()
        end = random.randint(1, self.get_announcements.get_announcements_num())
        b = []
        for i in range (end):
            start = self.common.get_random_int(self.get_announcements.get_announcements_num())
            b.append(self.announcements_id[start])
            b = list(set(b))
        body = [("utf8", "✓"), ("authenticity_token", self.csrf,), ("announcement_ids[]", b)]
        success = self.common.delete_response_json(url, body, '随机批量删除n条公告')
        if not success:
            return {}
        return self.response

    # 删除单个公告，随机删随机一条
    def delete_announcement(self):
        r = random.randint(1, self.get_announcements.get_announcements_num())
        self.announcements_id = self.get_announcements.get_announcements_list()
        rr = self.announcements_id[r-1]
        url = self.base_url + 'announcements/' + str(rr)
        body = {
            '_method': 'delete',
            'authenticity_token': self.csrf
        }
        response = self.common.post_response_json(url, body, '随机删除一条公告')
        return response
