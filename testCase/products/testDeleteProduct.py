# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class DeleteProduct:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.products_id =[]
        pass

    # 在产品详情页面删除产品
    def delete_product (self,product_id):
        url = self.base_url + 'products/' + str(product_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '在产品详情页面删除产品')

    # 删除产品分类
    def delete_product_category(self,product_category_id):
        url = self.base_url  + 'api/product_categories/' + str(product_category_id)
        body = {
            '_method': 'delete',
            'authenticity_token': self.csrf
        }
        response = self.common.delete_response_json(url,body,'删除产品分类')


      #批量删除产品
    def bulk_delete_products(self, product_ids):
        url = self.base_url + 'products/bulk_delete'
        body = {
            'product_ids[]':product_ids,
            'authenticity_token': self.csrf
        }
        response = self.common.delete_response_json(url, body, '批量删除产品')
        if not response:
            return {}
        self.response = response
        return self.response.json()


    #获取当前页的product id
    # def get_product_ids(self):
    #     url = self.base_url + 'products'
    #     body = {
    #         'scope':'all_own',
    #         'section_only':'true'
    #     }
    #     response = self.common.get_response_json(url, body, '删除合同时获取所有合同')
    #     if not response:
    #         return {}
    #     self.response = response
    #     S = self.response.content
    #     soup = BeautifulSoup(S)
    #     checked_product = soup.find(attrs={'data-entity-table-name':'product'})
    #     if checked_product:
    #         a = str(checked_product)
    #         product_id_list = re.findall(r"data-id=\"(.*?)\">",a)
    #         return product_id_list