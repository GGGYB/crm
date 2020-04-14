from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from .testGetAnnouncement import GetAnnouncement

class TopCancelTopAnnouncement:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.get_announcements = GetAnnouncement(cookie, csrf)
        self.announcements_id = []
        self.params = ''
        pass

    # 置顶公告，这里置顶第一条
    def top_announcement(self):
        self.announcements_id = self.get_announcements.get_announcements_list()
        rr = self.announcements_id[0]
        url = self.base_url + 'announcements/' + str(rr) + '/mark_as_top'
        body = {}
        response = self.common.put_response_json(url, body, '置顶某个公告')
        return  response

    # 取消公告置顶，这里取消第一条
    def cancel_top_announcement(self):
        self.announcements_id = self.get_announcements.get_announcements_list()
        url = self.base_url + 'announcements/' + str(self.announcements_id[0]) + '/cancel_top'
        body = {}
        response = self.common.put_response_json(url, body, '取消置顶某个公告')
        return response