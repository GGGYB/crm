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
from .testUpdateOrganization import UpdateOrganization



class Organization:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.update_organization = UpdateOrganization(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def testOrganization(self):
        self.update_organization.update_organization()




