# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
import importlib.util
from decimal import Decimal as D
from commons import common
from commons.const import const

class AddProduct:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.products_id =[]
        self.params = ''
        pass

    # 新增1级产品分类
    def add_first_product_catogory(self):
        url = self.base_url + 'api/product_categories.json'
        body = {
            'authenticity_token': self.csrf,
            'product_category[name]':'产品分类%s' %self.common.get_random_int(9999)
        }
        response = self.common.post_response_json(url, body, '新增1级产品分类 ')
        if not response:
            return {}
        product_catogory_id = response.json()['data']['id']
        return product_catogory_id

     # 新增2级产品分类
    def add_second_product_catogory(self):
        url = self.base_url + 'api/product_categories.json'
        body = {
            'product_category[parent_id]':self.add_first_product_catogory(),
            'authenticity_token': self.csrf,
            'product_category[name]':'产品分类%s' %self.common.get_random_int(9999)
        }
        response = self.common.post_response_json(url, body, '新增2级产品分类')
        if not response:
            return {}
        product_catogory_id = response.json()['data']['id']
        return product_catogory_id

    #新增产品
    def add_products(self,product_catogory):
        url = self.base_url + 'api/products'
        body = {
            'utf8':'✓',
            'authenticity_token': self.csrf,
            'product[id]':'',
            'product[name]': '产品%s' %self.common.get_random_int(9999),
            'product[product_no]': 'P00%s' %self.common.get_random_int(9999),
            'product[standard_unit_price]': '500',
            'product[sale_unit]': '488',
            'product[unit_cost]': '420',
            'product[product_category_id]':product_catogory,
            'product[introduction]': 'test%s'%self.common.get_random_int(9999),
            'product[numeric_asset_dc3135b0]': '244',
            'product[numeric_asset_918fc737]':'',
            'product[datetime_asset_7af968df]':'',
        }
        response = self.common.post_response_json(url, body, '新增产品 ')
        if not response:
            return {}
        self.response = response
        products_id = self.response.json()['id']
        return products_id