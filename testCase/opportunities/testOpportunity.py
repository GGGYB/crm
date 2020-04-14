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
from .testSettingsOpportunityApproval import Approvals
from .testAddOpportunity import AddOpportunities
from .testGetOpportunity import GetOpportunities
from .testUpdateOpportunity import UpdateOpportunities
from .testDeleteOpportunity import DeleteOpportunities

class Opportunities:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.add = AddOpportunities(cookie, csrf)
        self.get_opportunitie = GetOpportunities(cookie, csrf)
        self.update_opportunitie = UpdateOpportunities(cookie, csrf)
        self.delete_opportunitie = DeleteOpportunities(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.event_id =''
        pass

    def testOpportunities(self):
        self.add.add_opportunities()
        # self.testApprovalOpportunitie()
        scopes = self.get_opportunitie.opportunities_get_scopes()
        print (scopes)
        # self.filters.filters_by_business('Opportunities', scopes)
        self.filters.filters_by_business('jihuis', scopes)
        for scope in scopes:
            self.testUpdateOpportunities(scope)
            self.testDeletOpportunitie(scope)
            self.testCloseOpportunitiesApprovals()

    def testAddOpportunitie(self):
        self.testOpenOpportunitiesApprovals()
        self.applying_opportunitie = self.add.add_applying_opportunitie()
        self.testCloseOpportunitiesApprovals()
        opportunity_id = self.add.add_opportunities()
        self.add.add_event_for_opportunitie(opportunity_id)
        self.event_id =self.add.add_event_for_opportunitie(opportunity_id)
        self.testCloseOpportunitiesApprovals()

    def testGetOpportunities(self, scopes):
        self.testCloseOpportunitiesApprovals()
        self.filters.filters_by_business('Opportunities', scopes)
        opportunity_id = self.add.add_opportunities()
        self.get_opportunitie.opportunitie(opportunity_id)
        self.get_opportunitie.opportunities_get_scopes()

    def testDeletOpportunitie(self, scope):
        opportunity_ids = []
        for i in range(2):
            opportunity_ids.append(self.add.add_opportunities())
            if i<2:
                self.delete_opportunitie.delete_opportunitie(opportunity_ids[i])
        self.update_opportunitie.opportunities_field_update(scope, opportunity_ids)
        self.delete_opportunitie.delete_opportunities(opportunity_ids)


    #编辑商机
    def testUpdateOpportunities(self, scopes):
        for scope in scopes:
            opportunity_ids = []
            for i in range(3):
                opportunity_ids.append(self.add.add_opportunities())
            self.update_opportunitie.update_opportunities_by_scope(scope, opportunity_ids)

    #删除商机
    def testDeleteOpportunities(self):
        #删除单个商机
        opportunity_id = self.add.add_opportunities()
        self.delete_opportunitie.delete_opportunitie(opportunity_id)
        #批量删除商机
        opportunity_ids = []
        for i in range(2):
            opportunity_ids.append(self.add.add_opportunities())
        self.delete_opportunitie.delete_opportunities(opportunity_ids)

    #打开审批
    def testOpenOpportunitiesApprovals(self):
        _open_approvals = Approvals(self.cookie, self.csrf)
        _open_approvals.open_opportunitie_approval()

    #关闭审批
    def testCloseOpportunitiesApprovals(self):
        _close_approvals = Approvals(self.cookie, self.csrf)
        _close_approvals.close_opportunitie_approval()

    # 审批商机的操作
    def testApprovalOpportunitie(self):
        approve_opportunitie = Approvals(self.cookie, self.csrf)
        self.testOpenOpportunitiesApprovals()
        applying_opportunity_id = []
        for i in range(4):
            applying_opportunity_id.append(self.add.add_applying_opportunitie())
        approve_opportunitie.approve_opportunitie(applying_opportunity_id[0])
        approve_opportunitie.deny_opportunities_approval(applying_opportunity_id[1])
        approve_opportunitie.cancel_opportunities_approval(applying_opportunity_id[2])
        self.testCloseOpportunitiesApprovals()

    # #审批商机的操作
    # def testApprovalOpportunitie(self):
    #     update_opportunitie = UpdateOpportunitie(self.cookie, self.csrf)
    #     # update_opportunitie = UpdateOpportunitie(self.cookie, self.csrf)
    #     self.testOpenOpportunitiesApprovals()
    #     applying_opportunity_id = []
    #     for i in range(3):
    #         applying_opportunity_id.append(self.add.add_applying_opportunitie())
    #     update_opportunitie.approve_opportunitie(applying_opportunity_id[0])
    #     update_opportunitie.deny_opportunitie_approve(applying_opportunity_id[1])
    #     self.testCloseOpportunitiesApprovals()