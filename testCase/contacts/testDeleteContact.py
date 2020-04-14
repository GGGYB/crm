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

class DeleteContacts:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.user_id = ''
        self.contact_id =[]
        pass

    #删除单个联系人
    def delete_contact(self, contact_id):
        url = self.base_url + 'contacts/'+str(contact_id)
        body = {
            '_method':'delete',
            'authenticity_token':self.csrf
        }
        response = self.common.post_response_json(url, body, '删除当前联系人')
        return response
    # #批量删除联系人
    def delete_contacts(self, scope, contact_ids):
        url = self.base_url + 'contacts/bulk_delete'
        body = {
            'contact_ids[]': contact_ids[0],
            'contact_ids[]': contact_ids[1],
            'authenticity_token': self.csrf
        }
        response = self.common.delete_response_json(url, body, '批量删除联系人')
        if not response:
            return {}