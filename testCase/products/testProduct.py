# -*- coding: utf-8 -*-
__author__ = 'Jun'

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
from .testAddProduct import AddProduct
from .testGetProduct import GetProduct
from .testUpdateProduct import UpdateProduct
from .testDeleteProduct import DeleteProduct

class Products:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.add = AddProduct(cookie, csrf)
        self._get_products = GetProduct(cookie, csrf)
        self._update_products = UpdateProduct(cookie, csrf)
        self._delete_products = DeleteProduct(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass


    def testProducts(self):
        product_second_catogory = self.add.add_second_product_catogory()
        product_first_category = self.add.add_first_product_catogory()
        product_id = self.add.add_products(product_second_catogory)
        product_id_list = []
        for i in range(3):
            product_id_list.append(self.add.add_products(product_second_catogory) )
        self.testGetProducts(product_id)
        self.testUpdateProduct(product_id,product_first_category,product_id_list)
        self.testDeleteProducts(product_id,product_second_catogory,product_id_list)


   # 新增产品
    def testAddProduct(self):
        product_catogory = self.add.add_second_product_catogory()
        self.add.add_products(product_catogory)

    # 获取产品
    def testGetProducts(self,product_id):
        self._get_products.get_product_ids()
        self._get_products.get_product_detail(product_id)
        self._get_products.get_product_attachment(product_id)

    # 更新产品
    def testUpdateProduct(self,product_id,product_catogory,product_ids):
        self._update_products.update_single_products(product_id,product_catogory)
        self._update_products.deactivate_single_product(product_id)
        self._update_products.activate_single_product(product_id)
        self._update_products.update_product_category_id(product_catogory)
        self._update_products.up_product_category_id(product_catogory)
        self._update_products.down_product_category_id(product_catogory)
        self._update_products.products_batch_update(product_catogory,product_ids)
        self._update_products.deactivate_batch_product(product_ids)
        self._update_products.activate_batch_product(product_ids)

    #删除产品
    def testDeleteProducts(self,product_id,product_catogory,product_ids):
        self._delete_products.delete_product(product_id)
        self._delete_products.bulk_delete_products(product_ids)
        self._delete_products.delete_product_category(product_catogory)

