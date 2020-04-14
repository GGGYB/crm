# -*- coding: utf-8 -*-

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
from testCase.approvals import testContractApproval as ContractApproval
from testCase.login import testLogin as login
from testCase.contracts import testAddContract as AddContract

class Approval:
    def __init__(self,):
        self.csrf = ""
        self.cookie = ""
        self.Login =login.Login()
        # self.contract_approval = ContractApproval(cookie, csrf)
        pass

    def testApproval_one(self):
        print ('=====')
        self.Login.login("18721277192", "222222","1234")
        self.Login.get_csrf_by_home_html()
        self.cookie = self.Login.cookie
        self.csrf = self.Login.csrf
        Approval =ContractApproval.ContractApproval(self.cookie,self.csrf)

        approval_role_first = ['superior', 'specified', 'specified_jointly', 'previous_superior']
        Approval.close_contract_approval()
        for i in range(len(approval_role_first)):
            if approval_role_first[i] == 'previous_superior':
                continue
            else:
                Approval.open_contract_approval()
                Approval.open_first_approval(approval_role_first[i], 'editable', '3971')
                testAddContract =AddContract.AddContract(self.cookie,self.csrf)
                id = testAddContract.add_applying_contract()
                testAddContract.contract_approval_two(id)

            def testApproval_contract_one(self):
                print('=====')
                self.Login.login("13701649176", "111111", "1234")
                self.Login.get_csrf_by_home_html()
                self.cookie = self.Login.cookie
                self.csrf = self.Login.csrf
                Approval = ContractApproval.ContractApproval(self.cookie, self.csrf)
                Approval.open_contract_approval()
                Approval.open_fist_approval("specified", 'editable', '3674')
                testAddContract = AddContract.AddContract(self.cookie, self.csrf)
                id = testAddContract.add_applying_contract()


        # Approval.close_contract_approval()
        # Approval.open_contract_approval()
        # Approval.open_fist_approval("specified",'editable','3674')
        # testAddContract =AddContract.AddContract(self.cookie,self.csrf)
        # id = testAddContract.add_applying_contract()








