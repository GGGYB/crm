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
import  time
import  string
from commons import common
from commons import filters
from commons.const import const
from .testGetLeadCommon  import  GetLeadCommonId
from .testUpdateLeadCommon import UpdateLeadCommonId
from testCase.leads import  testAddLead
from testCase.leads import testUpdateLead
from  testCase.leads import  testGetLeads
from  testCase.users import testGetUser




class LeadCommon:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.filters = filters.Filters(cookie, csrf)
        self.get_current_user = testGetUser.GetUser(cookie, csrf)
        self.get_lead_common = GetLeadCommonId(cookie, csrf)
        self.batch_update_lead_common = UpdateLeadCommonId(cookie, csrf)
        self.add_lead_ids = testAddLead.AddLead(cookie, csrf)
        self.get_lead_ids = testGetLeads.GetLeads(cookie, csrf)
        self.update_lead_ids = testUpdateLead.UpdateLeads(cookie, csrf)
        pass

    def  superior_lead_common(self):
        lead_id = self.get_lead_common.get_lead_common_id()
        self.filters.lead_common_filters(lead_id)
        lead_ids = []
        lead_ids_other = []
        for i in range(2):
            lead_ids.append(self.add_lead_ids.add_lead())
        self.update_lead_ids.mass_transfer_to_common_pool(lead_ids)
        time.sleep(2)
        self.batch_update_lead_common.operate_lead_common(lead_ids,lead_id)
        for i in range(5):
            lead_ids_other.append(self.add_lead_ids.add_lead())
        self.update_lead_ids.mass_transfer_to_common_pool(lead_ids_other)
        time.sleep(5)
        self.batch_update_lead_common.bulk_delete_lead_common(lead_ids_other,lead_id)

    def  basic_lead_common(self):
        lead_id = self.get_lead_common.get_lead_common_id()
        self.filters.lead_common_filters(lead_id)
        lead_ids = []
        for i in range(2):
            lead_ids.append(self.add_lead_ids.add_lead())
        self.update_lead_ids.mass_transfer_to_common_pool(lead_ids)
        time.sleep(5)
        self.batch_update_lead_common.take_singel_lead(lead_ids)
        time.sleep(5)
        self.batch_update_lead_common.bulk_take_lead(lead_ids,lead_id)




