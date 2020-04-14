# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from testCase.products.testGetProduct import GetProduct
from  testCase.products.testAddProduct import AddProduct


class UpdateProduct:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.get_product_ids = GetProduct(cookie, csrf)
        self.get_product_category_id = AddProduct(cookie, csrf)
        self.response = ''
        self.users_id = []
        self.products_id = []

    # 详情页面编辑单个产品
    def update_single_products(self,product_id,product_catogory):
        url = self.base_url + 'api/products/'+str(product_id)
        body = {
            'utf8':'✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'product[id]':product_id,
            'product[name]': '产品%s' %self.common.get_random_int(9999),
            'product[product_no]': 'P00%s' %self.common.get_random_int(9999),
            'product[standard_unit_price]': '500',
            'product[sale_unit]': '488',
            'product[unit_cost]': '420',
            'product[product_category_id]':product_catogory,
            'product[introduction]': 'test%s'%self.common.get_random_int(9999),
            'product[datetime_asset_aac8b7]':'2018-08-01 20:00',
        }
        response = self.common.post_response_json(url, body, '详情页面编辑单个产品 ')
        print(response)
        if not response:
            return {}
        product_id = response.json()['data']['id']
        return product_id

   # 在产品详情页面禁用产品
    def  deactivate_single_product(self,product_id):
        url  = self.base_url + 'products/' + str(product_id) + '/deactivate'
        body = {}
        response = self.common.put_response_json(url,body,"在产品详情页面禁用产品")

    # 在产品详情页面启用产品
    def activate_single_product(self, product_id):
        url = self.base_url + 'products/' + str(product_id) + '/activate'
        body = {}
        response = self.common.put_response_json(url, body, "在产品详情页面启用产品")

    # 编辑产品分类
    def update_product_category_id(self,product_category_id):
        url = self.base_url + 'api/product_categories/ '+ str(product_category_id) + '.json'
        body = {
            'authenticity_token': self.csrf,
            'product_category[name]': '产品分类%s' %self.common.get_random_int(9999)
        }
        response = self.common.put_response_json(url,body,'编辑产品分类')

    # 产品分类上移
    def up_product_category_id(self, product_category_id):
        url = self.base_url + 'api/product_categories/' + str(product_category_id) + '/position_move.json'
        body = {
           'product_category[position_action]': 'move_higher'
        }
        response = self.common.post_response_json(url,body,'产品分类上移')

    # 产品分类上移
    def down_product_category_id(self, product_category_id):
        url = self.base_url + 'api/product_categories/' + str(product_category_id) + '/position_move.json'
        body = {
            'product_category[position_action]': 'move_lower'
         }
        response = self.common.post_response_json(url, body, '产品分类上移')

   # 批量编辑产品信息
    def products_batch_update(self, product_catogory,product_ids):
        url = self.base_url + 'batch_edit/field_form'
        params = {
            'model': 'Product'
        }
        response = self.common.get_response_json(url, params, '打开编辑产品的窗扣')
        if response != False:
            soup = BeautifulSoup(response.text, 'html.parser')
            soup = str(soup)
            optional_field = soup.split('control-label')
            fields = re.findall(r"value=\"(.*?)\">", str(optional_field[1]))
            for i in range(len(fields)):
                if (fields[i] == 'product_category'):
                    fields_id =  fields[i]
            url = self.base_url + 'api/products/batch_update'
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'field_choice': fields_id,
                'product[' + fields_id + ']':product_catogory ,
                'ids[]':product_ids
            }
            response = self.common.put_response_json(url, body, '批量编辑产品')
            return response

    # 批量禁用产品
    def deactivate_batch_product(self,product_ids):
        url = self.base_url + 'products/bulk_deactivate'
        body = {
            'product_ids[]': product_ids,
            'authenticity_token': self.csrf
        }
        response = self.common.put_response_json(url,body,'批量禁用产品')

    # 批量启用产品
    def activate_batch_product(self,product_ids):
        url = self.base_url + 'products/bulk_activate'
        body = {
            'product_ids[]': product_ids,
            'authenticity_token': self.csrf
        }
        response = self.common.put_response_json(url,body,'批量启用产品')


    # 给当前产品添加附件
    # def add_attachment_for_product(self, product_id):
    #      url = self.base_url + 'attachments/' + str(product_id) + '/add_attachment'
    #      body = {
    #          'utf8': '✓',
    #          'authenticity_token': self.csrf,
    #          'klass': 'Product',
    #          'sub_type': 'file',
    #          'attachment_ids[]': '产品附件%s' % self.common.get_random_int(9999),
    #          'note': '产品附件%s' % self.common.get_random_int(9999)
    #      }
    #      self.common.post_response_json(url, body, '产品详情页添加附件')


    # 获取产品的id list
    def get_product_ids(self, scope):
        url = self.base_url + 'products'
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': 'products.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取所有的产品')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        checked_product = soup.find(attrs={'data-entity-table-name': 'product'})
        if checked_product:
            a = str(checked_product)
            product_ids = re.findall(r"data-id=\"(.*?)\">", a)
            return product_ids


