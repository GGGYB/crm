# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
import time
from commons import common
from commons.const import const
from testCase.login import testLogin as login
from testCase.users.testGetUser import GetUser
from testCase.opportunities.testAddOpportunity import AddOpportunities
from testCase.approvals.testApprovalSetting import ApprovalSettings
from testCase.opportunities.testGetOpportunity import GetOpportunities
class ApprovalCase:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.Login = login.Login()
        self.user = GetUser(cookie, csrf)
        self.add = AddOpportunities(cookie, csrf)
        self.approvalset = ApprovalSettings(cookie, csrf)
        self.sleeptime = 10
        pass

    # 实现多次登录登出实例化
    def login(self, username, password, role):
        _login1 = login.Login()
        _login1.login(username, password, role)
        _login1.get_csrf_by_home_html()
        _cookie1 = _login1.cookie
        _csrf1 = _login1.csrf
        dict = {}
        dict['cookie'] = _cookie1
        dict['csrf'] = _csrf1
        return dict


    def testCase1(self):
        print("开启一级审批，规则：负责人主管/指定用户（任意一人），超管审批(审批人/非审批人)")
        self.approvalset.close_opportunity_approval()
        approval_role = ['superior', 'specified']
        for i in range(len(approval_role)):
            self.approvalset.open_opportunity_approval()
            approval_role = ['2222409','2222396']
            for j in range(len(approval_role)):
                self.approvalset.open_first_approval('specified', 'cannot', approval_role[j])
                cookie_and_asrf = self.login("19112341234", "111111", "负责人")
                add = AddOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
                opportunity_id = add.add_applying_opportunities()
                self.GetOpportunities = GetOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批", "opportunityid:%s" % opportunity_id)
                approvalset_first = ApprovalSettings(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
                approvalset_first.cancel_opportunities_approval(opportunity_id)
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已撤销",
                                         "opportunityid:%s" % opportunity_id)
                add.re_add_applying_opportunities(opportunity_id)
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                         "opportunityid:%s" % opportunity_id)
                self.approvalset.deny_opportunities_approval(opportunity_id)
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已否决",
                                         "opportunityid:%s" % opportunity_id)
                add.re_add_applying_opportunities(opportunity_id)
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                         "opportunityid:%s" % opportunity_id)
                self.approvalset.approve_opportunity(opportunity_id)
                self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已通过",
                                         "opportunityid:%s" % opportunity_id)

    def testCase2(self):
        print("开启一级审批，规则：负责人主管/指定用户（任意一人），普通用户(审批人)")
        self.approvalset.close_opportunity_approval()
        approval_setting = ['superior','specified']
        for i in range(len(approval_setting)):
            _cookie_and_asrf = self.login('13312341234', "111111", "负责人主管")
            approvalset = ApprovalSettings(_cookie_and_asrf['cookie'], _cookie_and_asrf['csrf'])
            approvalset.open_opportunity_approval()
            approvalset.open_first_approval('specified', 'cannot', '2222409')
            cookie_and_asrf = self.login("19112341234", "111111", "负责人")
            add = AddOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            opportunity_id = add.add_applying_opportunities()
            self.GetOpportunities = GetOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批", "opportunityid:%s" % opportunity_id)
            approvalset_first = ApprovalSettings(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            approvalset_first.cancel_opportunities_approval(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已撤销",
                                     "opportunityid:%s" % opportunity_id)
            add.re_add_applying_opportunities(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                     "opportunityid:%s" % opportunity_id)
            approvalset_second = ApprovalSettings(_cookie_and_asrf['cookie'], _cookie_and_asrf['csrf'])
            approvalset_second.deny_opportunities_approval(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已否决",
                                     "opportunityid:%s" % opportunity_id)
            add.re_add_applying_opportunities(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                     "opportunityid:%s" % opportunity_id)
            approvalset_second.approve_opportunity(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已通过",
                                     "opportunityid:%s" % opportunity_id)

    def testCase3(self):
        print("开启一级审批，规则：负责人主管的主管，普通用户(审批人)")
        self.approvalset.close_opportunity_approval()
        approval_setting = ['superior', 'specified']
        for i in range(len(approval_setting)):
            _cookie_and_asrf = self.login('19012349125', "111111", "负责人主管的主管")
            approvalset = ApprovalSettings(_cookie_and_asrf['cookie'], _cookie_and_asrf['csrf'])
            approvalset.open_opportunity_approval()
            approvalset.open_first_approval('specified', 'cannot', '2222655')
            cookie_and_asrf = self.login("19112341234", "111111", "负责人")
            add = AddOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            opportunity_id = add.add_applying_opportunities()
            self.GetOpportunities = GetOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                     "opportunityid:%s" % opportunity_id)
            approvalset_first = ApprovalSettings(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
            approvalset_first.cancel_opportunities_approval(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已撤销",
                                     "opportunityid:%s" % opportunity_id)
            add.re_add_applying_opportunities(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                     "opportunityid:%s" % opportunity_id)
            approvalset_second = ApprovalSettings(_cookie_and_asrf['cookie'], _cookie_and_asrf['csrf'])
            approvalset_second.deny_opportunities_approval(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已否决",
                                     "opportunityid:%s" % opportunity_id)
            add.re_add_applying_opportunities(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                     "opportunityid:%s" % opportunity_id)
            approvalset_second.approve_opportunity(opportunity_id)
            self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已通过",
                                     "opportunityid:%s" % opportunity_id)

    def testCase4(self):
        print("开启一级审批，规则：多人会签，所有审批人去审批")
        self.approvalset.close_opportunity_approval()
        _cookie_and_asrf = self.login('19012349125', "111111", "负责人主管的主管")
        approvalset = ApprovalSettings(_cookie_and_asrf['cookie'], _cookie_and_asrf['csrf'])
        approvalset.open_opportunity_approval()
        approval_user = ['13312341234','19112341234']
        approvalset.open_first_approval('specified', 'cannot', approval_user)
        cookie_and_asrf = self.login("19112341234", "111111", "负责人")
        add = AddOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
        opportunity_id = add.add_applying_opportunities()
        self.GetOpportunities = GetOpportunities(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
        self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                 "opportunityid:%s" % opportunity_id)
        approvalset_first = ApprovalSettings(cookie_and_asrf['cookie'], cookie_and_asrf['csrf'])
        approvalset_first.cancel_opportunities_approval(opportunity_id)
        self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已撤销",
                                 "opportunityid:%s" % opportunity_id)
        add.re_add_applying_opportunities(opportunity_id)
        self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                 "opportunityid:%s" % opportunity_id)
        approvalset_first.deny_opportunities_approval(opportunity_id)
        self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已否决",
                                 "opportunityid:%s" % opportunity_id)
        add.re_add_applying_opportunities(opportunity_id)
        self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "待1级审批",
                                 "opportunityid:%s" % opportunity_id)
        # approvalset_first.approve_opportunity(opportunity_id)
        # self.common.check_string(self.GetOpportunities.opportunities_info(opportunity_id), "已通过",
        #                          "opportunityid:%s" % opportunity_id)


