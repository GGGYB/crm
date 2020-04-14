# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

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
from .testCommonFilterReport import CommonFilterReport

class ProductSalesStats:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.commonFilter = CommonFilterReport(cookie, csrf)
        pass

    #产品销售汇总报表
    def testProductSalesStatsByDimension(self):
        url = self.base_url + 'report_center/product_sales_stats'
        params = {}
        self.filtersReport(url, params)

    def filtersReport(self, url, params):
        self.commonFilter.filters_by_department(url, params, '销售预测报表:按照跟进部门搜索')
        self.commonFilter.filters_by_user(url, params, '销售预测报表:按照跟进人用户搜索')