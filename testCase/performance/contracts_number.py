from bs4 import BeautifulSoup
import os
import json
import requests
import random
import datetime
# import MySQLdb
import time
import re
import sys
from decimal import Decimal as D
from commons import common
from commons.const import const
from commons import filters
from testCase.login import testLogin as login
from testCase.contracts import testContract as contracts
from testCase.contracts import testSettingsContractsApproval as ContractsApproval
from testCase.contracts import testAddContract as AddContract
from testCase.contracts import testDeleteContract as DeleteContract
from testCase.performance.result_contracts_number import result_contract_number
from testCase.performance.result_contracts_number import result_contract_number_departments



class contracts_number:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        # self.userinfo_super = {'username': '15639356523', 'password': 'Ab123456','role':'超管'}
        self.userinfo_super = {'username': '18049905933', 'password': 'Ik123456', 'role': '超管'}
        self.sign_date_list = ['2019-01-31','2019-03-31','2019-05-31','2019-07-31','2019-09-30','2019-11-30']
        self.total_amount_list = [[110, -20], [260, -220], [310, 220], [410, 420], [510, -520], [1, 2], [200, 100],
                                  [220, 230]]
        self.userinfo_list = const.USER
        pass

    def case_1(self):
        self.current_case = 'case 1'
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie =_login.cookie
        self.csrf = _login.csrf
        _ContractsApproval =ContractsApproval.Approvals(self.cookie,self.csrf)
        _ContractsApproval.close_contract_approval()
        a =0
        for userinfo in self.userinfo_list:
            print (userinfo['username'])
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _AddContract = AddContract.AddContract(self.cookie,self.csrf)
            _ContractsApproval =ContractsApproval.Approvals(self.cookie,self.csrf)
            _DeleteContracts =DeleteContract.DeleteContract(self.cookie,self.csrf)
            # contracts_list =_DeleteContracts.get_contract_ids()
            # print (contracts_list)
            a= a+1
            for i in range(6):
                for b in range(a):
                    if userinfo['username'] == '13799999999' and i>=3 :
                        #添加合同
                        _AddContract.add_contracts(sign_date=self.sign_date_list[i],
                                                   total_amount=self.total_amount_list[a - 1][0] * (i+1),DepartmentId=1)

                    else:
                        # 添加合同
                        _AddContract.add_contracts(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1))

        _login.login(self.userinfo_super['username'], self.userinfo_super['password'],
                        self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
        _ContractsApproval.open_contract_approval()
        a = 0
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            print (userinfo['username'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _AddContract = AddContract.AddContract(self.cookie,self.csrf)
            _ContractsApproval =ContractsApproval.Approvals(self.cookie,self.csrf)
            a = a+1
            for i in range(6):
                if userinfo['username'] == '13799999999' and i>=3:
                    for b in range(a):
                        # 审批通过的合同
                        _ContractsApproval.verify_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying',DepartmentId=1)[0])

                    # 待审批的合同
                    _AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying',DepartmentId=1)


                    # 审批通过后否决
                    contracts_id = _AddContract.add_contracts(sign_date=self.sign_date_list[i],
                                                              total_amount=self.total_amount_list[a - 1][0] * (i + 1),
                                                              approve_status='applying',DepartmentId=1)[0]
                    _ContractsApproval.verify_contracts(contracts_id)
                    print(_AddContract.contracts_id)
                    _ContractsApproval.deny_contracts(contracts_id)

                     # 审批否决的合同
                    _ContractsApproval.deny_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],
                                                                                 total_amount=self.total_amount_list[a - 1][0] * (i + 1),
                                                                                 approve_status='applying',DepartmentId=1)[0])

                    # 合同撤销
                    _ContractsApproval.cancel_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=
                                                                                   self.total_amount_list[a - 1][0] * (i + 1),
                                                                                   approve_status='applying',DepartmentId=1)[0])

                    # 添加草稿
                    _AddContract.add_contracts(sign_date=self.sign_date_list[i],
                                               total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='draft',DepartmentId=1)



                else:
                    # 待审批的合同
                    _AddContract.add_contracts(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying')
                    for b in range(a):
                        # 审批通过的合同
                        _ContractsApproval.verify_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying')[0])

                    # 审批通过后否决
                    contracts_id=_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying')[0]
                    _ContractsApproval.verify_contracts(contracts_id)
                    print (_AddContract.contracts_id)
                    _ContractsApproval.deny_contracts(contracts_id)

                    # 审批否决的合同
                    _ContractsApproval.deny_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying')[0])
                     # 合同撤销
                    _ContractsApproval.cancel_contracts(_AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='applying')[0])
                    # 添加草稿
                    _AddContract.add_contracts(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),approve_status='draft')

    def case_2(self):
        self.current_case = 'case 2'
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie =_login.cookie
        self.csrf = _login.csrf
        _ContractsApproval =ContractsApproval.Approvals(self.cookie,self.csrf)
        _ContractsApproval.close_contract_approval()
        _DeleteContracts = DeleteContract.DeleteContract(self.cookie, self.csrf)
        b =_DeleteContracts.get_contract_ids()
        page =b[0][0]
        print (page)
        for i in range(int(page)):
             c =_DeleteContracts.get_contract_ids()
             contracts_list = c[1]
             for contracts in contracts_list:
                 _DeleteContracts.delete_contract(contracts)




if __name__ == '__main__':
    _contracts_number =contracts_number()
    # os.remove('status_code_ok.txt')
    # os.remove('status_code.txt')
    # _contracts_number.case_2()
    # _contracts_number.case_1()

    #创建合同数的对象
    _contract_number = result_contract_number.result_contract_number_user()
    #按用户 合同数 报表筛选
    _contract_number.contract_number_baobiao()
    #按用户 合同数 工作台筛选
    _contract_number.contract_number_gongzuotai()
    # #按部门 合同数 报表筛选
    _contract_number_departments=result_contract_number_departments.result_contract_number_departments()
    _contract_number_departments.contract_number_d_baobiao()











