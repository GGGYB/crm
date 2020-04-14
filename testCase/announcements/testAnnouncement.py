from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
import sys
from decimal import Decimal as D
from commons import common
from commons.const import const
from commons import filters
from .testAddAnnouncement import AddAnnouncement
from .testTopAnnouncement import TopCancelTopAnnouncement
from .testUpdateAnnouncement import UpdateAnnouncement
from .testDeleteAnnouncement import DeleteAnnouncement
from .testGetAnnouncement import GetAnnouncement


class Announcements:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.get_announcement = GetAnnouncement(cookie, csrf)
        self.add_announcement = AddAnnouncement(cookie, csrf)
        self.update_annnouncement = UpdateAnnouncement(cookie, csrf)
        self.top_cancel_top_announcement = TopCancelTopAnnouncement(cookie,csrf)
        self.delete_announcement = DeleteAnnouncement(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def testAnnouncements(self):
        self.get_announcement.get_announcements_num()
        self.add_announcement.add_announcements_all()
        self.add_announcement.add_announcements_department()
        self.add_announcement.add_announcements_role()
        self.update_annnouncement.update_announcement()
        self.top_cancel_top_announcement.top_announcement()
        self.top_cancel_top_announcement.cancel_top_announcement()
        self.delete_announcement.batch_delete_announcements()
        self.delete_announcement.delete_announcement()







