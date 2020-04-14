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
from .testSettingsContractsApproval import Approvals
from .testAddContract import AddContract
from .testGetContract import GetContracts
from .testUpdateContract import UpdateContract
from .testDeleteContract import DeleteContract

class Contracts:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.filters = filters.Filters(cookie, csrf)
        self.add = AddContract(cookie, csrf)
        self.get_contract = GetContracts(cookie, csrf)
        self.update_contract = UpdateContract(cookie, csrf)
        self.delete_contract = DeleteContract(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.event_id =''
        self.contract_id = ''
        pass


    def testContracts(self):
        self.testAddContract()
        self.testApprovalContract()
        scopes = self.get_contract.contracts_get_scopes()
        self.filters.contract_filters_by_business('contracts', scopes)
        for scope in scopes:
            self.testGetContracts(scope)
            self.testUpdateContracts(scope)
            # self.testCloseContractsApprovals()
            self.testDeletContract(scope)


    def testAddContract(self):
        self.testOpenContractsApprovals()
        self.applying_contract = self.add.add_applying_contract()
        self.testCloseContractsApprovals()
        self.add.add_contracts()
        contract_id = self.add.add_contracts()
        self.event_id =self.add.add_event_for_contract(contract_id)
        # self.testCloseContractsApprovals()


    def testGetContracts(self, scopes):
        self.testCloseContractsApprovals()
        self.filters.contract_filters_by_business('Contracts', scopes)
        contract_id = self.add.add_contracts()
        self.get_contract.contract(contract_id)
        self.get_contract.contracts_get_scopes()


    def testDeletContract(self, scope):
        contract_ids = []
        for i in range(2):
            contract_ids.append(self.add.add_contracts())
            if i<2:
                self.delete_contract.delete_contract(contract_ids[i])
        self.update_contract.contracts_field_update(scope, contract_ids)
        self.delete_contract.delete_contracts(contract_ids)

    #编辑合同
    def testUpdateContracts(self, scopes):
        for scope in scopes:
            contract_ids = []
            for i in range(3):
                contract_ids.append(self.add.add_contracts())
            self.update_contract.update_contracts_by_scope(scope, contract_ids)

        # self.update_contract.update_event_todo(event_id)
    #删除合同
    def testDeleteContracts(self):
        #删除单个合同
        contract_id = self.add.add_contracts()
        self.delete_contract.delete_contract(contract_id)
        #批量删除合同
        contract_ids = []
        for i in range(2):
            contract_ids.append(self.add.add_contracts())
        self.delete_contract.delete_contracts(contract_ids)

    #打开审批
    def testOpenContractsApprovals(self):
        _open_approvals = Approvals(self.cookie, self.csrf)
        _open_approvals.open_contract_approval()

    #关闭审批
    def testCloseContractsApprovals(self):
        _close_approvals = Approvals(self.cookie, self.csrf)
        _close_approvals.close_contract_approval()

    #审批合同的操作
    def testApprovalContract(self):
        update_contract = UpdateContract(self.cookie, self.csrf)
        self.testOpenContractsApprovals()
        applying_contract_id = []
        for i in range(3):
            applying_contract_id.append(self.add.add_applying_contract())
        # update_contract.approve_contract(applying_contract_id[0])
        # update_contract.deny_contract(applying_contract_id[1])
        self.testCloseContractsApprovals()