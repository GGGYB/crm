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

class Approvals:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def open_received_payment_approval(self):
        url = self.base_url + 'settings/received_payment_approve/update'
        params = {
            'received_payment_approve_config[enable_received_payment_approve]': '1'
        }
        self.common.put_response_json(url, params, '开启审批')


    def close_received_payment_approval(self):
        url = self.base_url + 'settings/received_payment_approve/update'
        params = {
            'received_payment_approve_config[enable_received_payment_approve]': '0'
        }
        self.common.put_response_json(url, params, '开启审批')

    # 回款金额审批通过
    def received_payments_verify(self, received_payment_id):
        url = self.base_url + 'api/received_payments/%s/approve' % received_payment_id
        body = {
              'utf8': '✓',
            'authenticity_token': self.csrf,
            '_method':'put',
            'approve_description':'审批通过',
            'received_payment[notify_user_ids][]':''
        }
        success = self.common.post_response_json(url, body, 'received payments verify')
        if not success:
            return {}
        return received_payment_id

    # 回款金额审批通过否决
    def received_payments_deny(self, received_payment_id):
        url = self.base_url +  'api/received_payments/%s/deny' % received_payment_id
        body = {
             'utf8': '✓',
            'authenticity_token': self.csrf,
            '_method':'put',
            'approve_description':'审批否决',
        }
        success = self.common.post_response_json(url, body, 'received payments')
        if not success:
            return {}
        return received_payment_id

