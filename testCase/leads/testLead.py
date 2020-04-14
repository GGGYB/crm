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
from commons import filters
from .testAddLead import AddLead
from .testDeleteLead import DeleteLeads
from .testGetLeads import GetLeads
from .testUpdateLead import UpdateLeads

class Leads:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.add_lead = AddLead(cookie, csrf)
        self.delete_lead = DeleteLeads(cookie, csrf)
        self.get_lead = GetLeads(cookie, csrf)
        self.update_lead =UpdateLeads(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def testLeads(self):
        self.add_lead.add_lead()
        # self.add_lead.leads_camcard_launch()  扫描名片不能使用
        # self.get_lead.duplicate_leads()
        # self.testAdd()
        # scopes = self.get_lead.get_all_scope()
        # self.filters.filters_by_business('leads', scopes)
        # for scope in scopes:
        #     self.testUpdateLead(scope)
        #     self.testDeletLead(scope)


    def testAdd(self):
        lead_id = self.add_lead.add_lead()
        id = self.add_lead.add__event_for_lead(lead_id)

    def testDeletLead(self, scope):
        lead_ids = []
        for i in range(5):
            lead_ids.append(self.add_lead.add_lead())
            if i<2:
                self.delete_lead.delete_lead(lead_ids[0])
                lead_ids.remove(lead_ids[0])
        self.update_lead.batch_update_leads(scope, lead_ids)
        self.delete_lead.delete_leads(scope, lead_ids)

    def testUpdateLead(self, scope):
        lead_id = self.add_lead.add_lead()
        self.update_lead.write_revisit_log(scope, lead_id)
