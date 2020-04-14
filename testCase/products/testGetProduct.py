# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
# import MySQLdb
import re
from decimal import Decimal as D
from commons import common
from commons.const import const

class GetProduct:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.csrf1 = ''
        self.given_cookie = ''  # 用于存储人工指定的cookie，一旦设置后，就不使用页面内获取的cookie
        self.authorization = ''
        self.user_id = ''
        self.products_id =[]
        self.sql_host = 'rdscbq34656z0ix59br0.mysql.rds.aliyuncs.com'
       # 某些post或是get时要求header里带的信息，应该是一个帐户对应于唯一一个
        # 格式类似于：'Token token=cb5e0c1db161fe92a7f4ce67754821, uid=b9d28be2d18075de7435'
        pass

    #获取产品ID
    def get_product_ids(self):
        url = self.base_url + 'products/section.js'
        body = {
            '_': '1533123646516'
        }
        response = self.common.get_response_json(url, body, '获取当前页的产品')
        if not response:
            return {}
        soup = BeautifulSoup(response.text, "html.parser")
        soup = str(soup)
        soup=soup.split(' ' 'checkbox-custom' ' ')[0]
        products_id_list = re.findall(r'\"product_id\":(.*?),', str(soup))
        print(products_id_list)
        return products_id_list

    # #导出所选产品
    # def export_selected_products(self, scope):
    #     products_ids = self.products_ids()
    #     url = self.base_url + 'products?export_page=1&amp;format_type=calculate_export_pages&amp;order=asc&amp;per_page=10&amp;scope='+scope+'&amp;sort=products.updated_at+desc&amp;type=advance&selected_ids%5B%5D='+products_ids[0]+'&selected_ids%5B%5D='+products_ids[1]+'&format=js'
    #     self.common_get_resonse_json(url, 'export_selected_products')
    #     url = self.base_url + 'products.js?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&selected_ids%5B%5D='+products_ids[0]+'&selected_ids%5B%5D='+products_ids[1]+'&sort=products.updated_at+desc&type=advance'
    #     self.common_get_resonse_json(url, 'excute download export selected file')
    # #导出全部产品
    # def export_all_products(self, scope):
    #     url = self.base_url + 'products?format_type=calculate_export_pages&order=asc&per_page=10&scope='+scope+'&sort=products.updated_at+desc&type=advance'
    #     self.common_get_resonse_json(url, 'export_all_products')
    #
    #     #点击下载文档
    #     url = self.base_url + 'products?export_page=1&format_type=xlsx&order=asc&per_page=10&scope='+scope+'&sort=products.updated_at+desc&type=advance'
    #     self.common_get_resonse_json(url, 'excute download export all products file')

    #获取产品详情
    def get_product_detail(self,product_id):
        url = self.base_url + 'products/'+ str(product_id)
        body = {}
        response = self.common.get_response_json(url, body, '获取产品详情')
        return product_id

    #查看产品下的附件
    def get_product_attachment(self,product_id):
        url = self.base_url + 'api/attachments'
        params = {
            'page':'',
            'perPage':15,
            'entity_id':product_id,
            'klass':'Product',
            'sub_type': 'file'
        }
        self.common.get_response_json(url, params, '查看当前产品的附件')

