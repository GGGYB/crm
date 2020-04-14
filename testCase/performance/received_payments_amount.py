from commons.const import const
from testCase.login import testLogin as login
from testCase.contracts import testSettingsContractsApproval as ContractsApproval
from testCase.contracts import testAddContract as AddContract
from testCase.received_payment_center import testSettingsReceivedPaymentApproval as ReceivedPaymentApproval
from testCase.received_payment_center import testAddReceivedPayments as AddReceivedPayments
from testCase.contracts import testDeleteContract as DeleteContract
from testCase.performance.contract_rank import result_received_payments_amount_user_case1
from testCase.performance.contract_rank import result_received_payments_amount_user_case2
from testCase.performance.contract_rank import result_received_payments_amount_department_case1
from testCase.performance.contract_rank import result_received_payments_amount_department_case2


class received_payment_amount:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        self.userinfo_super = {'username': '18049905933', 'password': 'Ik123456','role':'超管'}
        self.sign_date_list = ['2019-01-31', '2019-03-31', '2019-05-31', '2019-07-31', '2019-09-30', '2019-11-30']
        self.total_amount_list = [[110, -20], [260, -220], [310, 220], [410, 420], [510, -520], [1, 2], [200, 100],
                                  [220, 230]]
        self.userinfo_list = const.USER
        pass

    def case_1(self):
        self.current_case = 'case 1'
        _login = login.Login()
        a = 0
        # # 超管登录 关闭合同回款审批，新增回款===================================
        # _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie =_login.cookie
        self.csrf = _login.csrf
        _ContractsApproval =ContractsApproval.Approvals(self.cookie,self.csrf)
        _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
        #关闭合同审批和回款审批
        _ContractsApproval.close_contract_approval()
        _ReceivedPaymentApproval.close_received_payment_approval()
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie = _login.cookie
            self.csrf = _login.csrf
            _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
            _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
            _AddReceivedPayments = AddReceivedPayments.AddReceivedPayment(self.cookie, self.csrf)
            _AddContract = AddContract.AddContract(self.cookie, self.csrf)
            a = a + 1
            # 添加一个合同
            if userinfo['username'] == '13799999999' :
                # 新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                # 用户6--合同所属部门：设计部
                contract_return_id = _AddContract.add_contracts(DepartmentId=1)
                for i in range(6):
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                #用户6--合同所属部门：产品部
                contract_return_id = _AddContract.add_contracts(DepartmentId=0)
                for i in range(6):
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])

            else:
                # 新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                contract_return_id = _AddContract.add_contracts(DepartmentId=0)  # id[0]为合同id id[1]为客户id
                for i in range(6):
                    # 添加新增回款记录
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                               amount=self.total_amount_list[a-1][0] * (i+1),
                                                               customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                               amount=self.total_amount_list[a - 1][1] * (i + 1),
                                                               customer_id=contract_return_id[1])

        # 超管登录 关闭合同审批，开启回款审批，=========================
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'],
                        self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
        _ReceivedPaymentApproval.open_received_payment_approval()
        a = 0
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
            _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
            _AddReceivedPayments = AddReceivedPayments.AddReceivedPayment(self.cookie, self.csrf)
            _AddContract = AddContract.AddContract(self.cookie, self.csrf)
            a= a+1
            if userinfo['username'] == '13799999999' :
                    # 新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                    contract_return_id = _AddContract.add_contracts(DepartmentId=1)
                    for i in range(6):
                    # 新增审批通过后的回款
                        _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][0] * (i + 1),customer_id =contract_return_id[1]))
                        _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][1] * (i + 1),customer_id =contract_return_id[1]))
                    contract_return_id = _AddContract.add_contracts(DepartmentId=0)
                    for i in range(6):
                        _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
                        _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
                    # 新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                    contract_return_id =_AddContract.add_contracts(DepartmentId=1)
                    for i in range(6):
                        # 新增待审批的回款
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][0] * (i + 1),customer_id =contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i], amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    contract_return_id = _AddContract.add_contracts(DepartmentId=0)
                    for i in range(6):
                        # 新增待审批的回款
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    # 新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                    contract_return_id =_AddContract.add_contracts(DepartmentId=1)
                    for i in range(6):
                        # 新增审批否决后的回款
                        _ReceivedPaymentApproval.received_payments_deny(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][0] * (i + 1),customer_id =contract_return_id[1]))
                        _ReceivedPaymentApproval.received_payments_deny(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][1] * (i + 1),customer_id =contract_return_id[1]))
                    contract_return_id =_AddContract.add_contracts(DepartmentId=0)
                    for i in range(6):
                        _ReceivedPaymentApproval.received_payments_deny(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                                       amount=self.total_amount_list[a - 1][0] * (i + 1),
                                                                       customer_id=contract_return_id[1]))
                        _ReceivedPaymentApproval.received_payments_deny(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                                       amount=self.total_amount_list[a - 1][1] * (i + 1),
                                                                       customer_id=contract_return_id[1]))
                    contract_return_id = _AddContract.add_contracts(DepartmentId=1)
                    for i in range(6):
                            # 新增审批通过后驳回的回款
                            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][0] * (i + 1),customer_id =contract_return_id[1])))
                            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date =self.sign_date_list[i],amount =self.total_amount_list[a - 1][1] * (i + 1),customer_id =contract_return_id[1])))
                    contract_return_id = _AddContract.add_contracts(DepartmentId=0)
                    for i in range(6):
                        # 新增审批通过后驳回的回款
                        _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                                           amount=self.total_amount_list[a - 1][0] * (i + 1), customer_id=contract_return_id[1])))
                        _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                                           amount=self.total_amount_list[a - 1][1] * (i + 1), customer_id=contract_return_id[1])))

            else:
                # 添加一个合同
                contract_return_id = _AddContract.add_contracts()
                for i in range(6):
                    # 新增审批通过后的回款
                    _ReceivedPaymentApproval.received_payments_verify(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
                    _ReceivedPaymentApproval.received_payments_verify(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
                contract_return_id = _AddContract.add_contracts()
                for i in range(6):
                    # 新增待审批的回款
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                # # 添加一个合同
                contract_return_id = _AddContract.add_contracts()
                for i in range(6):
                    # 新增审批否决后的回款
                    _ReceivedPaymentApproval.received_payments_deny(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
                    _ReceivedPaymentApproval.received_payments_deny(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
                # #添加一个合同
                contract_return_id = _AddContract.add_contracts()
                for i in range(6):
                    # 新增审批通过后驳回的回款
                    _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])))
                    _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])))

    def case_2(self):
        _login = login.Login()
        a = 0
        # 超管登录 合同审批开启 回款审批关闭，新增回款===================================
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
        _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
        # 开启合同审批和 关闭回款审批
        _ContractsApproval.open_contract_approval()
        _ReceivedPaymentApproval.close_received_payment_approval()
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            print (userinfo['username'])
            self.cookie = _login.cookie
            self.csrf = _login.csrf
            _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
            _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
            _AddReceivedPayments = AddReceivedPayments.AddReceivedPayment(self.cookie, self.csrf)
            _AddContract = AddContract.AddContract(self.cookie, self.csrf)
            a = a + 1
            if userinfo['username'] == '13799999999':
                for b in range(2):
                    # 添加一个待审批的合同(p1-1)；新增合同后返回的合同id和客户id：contract_return_id[0]为合同id contract_return_id[1]为客户id
                    contract_return_id = _AddContract.add_contracts(DepartmentId=b,approve_status='applying')
                    _ContractsApproval.verify_contracts(contract_return_id[0])
                    # print (contract_return_id[0])
                    for i in range(6):
                        # 添加新增回款记录
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    print (u'合同审批通过，回款关闭，数据完成================================')

                    # 添加一个待审批的合同(p2-1)
                    contract_return_id = _AddContract.add_contracts(DepartmentId=b, approve_status='applying')
                    for i in range(6):
                        # 添加新增回款记录
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    print(u'合同待审批，回款关闭，数据完成================================')

                    # 添加一个待审批的合同 合同驳回(P3-1)
                    contract_return_id = _AddContract.add_contracts(DepartmentId=b,approve_status='applying')  # id[0]为合同id id[1]为客户id
                    # print(contract_return_id)
                    # 审批通过
                    _ContractsApproval.verify_contracts(contract_return_id[0])
                    _ContractsApproval.deny_contracts(contract_return_id[0])
                    for i in range(6):
                        # 添加新增回款记录
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    # 添加一个撤销的合同(p4-1)
                    contract_return_id = _AddContract.add_contracts(DepartmentId=b, approve_status='applying')
                    for i in range(6):
                        # 添加新增回款记录
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                        _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                        amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                    _ContractsApproval.cancel_contracts(contract_return_id[0])

                    print(u'合同待撤销，回款关闭，数据完成================================')
            else:
                # 添加一个待审批的合同(p1-1)
                contract_return_id = _AddContract.add_contracts(DepartmentId=0, approve_status='applying')
                # 审批通过
                _ContractsApproval.verify_contracts(contract_return_id[0])
                print(contract_return_id[0])
                for i in range(6):
                    # 添加新增回款记录
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                print(u'合同审批通过，回款关闭，数据完成================================')

                # 添加一个待审批的合同(p2-1)
                contract_return_id = _AddContract.add_contracts(DepartmentId=0, approve_status='applying')
                for i in range(6):
                    # 添加新增回款记录
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                print(u'合同待审批，回款关闭，数据完成================================')

                # 添加一个待审批的合同 合同通过后驳回(P3-1)
                contract_return_id = _AddContract.add_contracts(DepartmentId=0, approve_status='applying')
                # 审批通过
                _ContractsApproval.verify_contracts(contract_return_id[0])
                _ContractsApproval.deny_contracts(contract_return_id[0])
                for i in range(6):
                    # 添加新增回款记录
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                # 添加一个撤销的合同(p4-1)
                contract_return_id = _AddContract.add_contracts(DepartmentId=0, approve_status='applying')
                for i in range(6):
                    # 添加新增回款记录
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])
                _ContractsApproval.cancel_contracts(contract_return_id[0])

                print(u'合同待撤销，回款关闭，数据完成================================')

        #超管登录 合同审批开启 回款审批开启，新增回款===================================
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
        _ReceivedPaymentApproval.open_received_payment_approval()
        a = 0
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie = _login.cookie
            self.csrf = _login.csrf
            _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
            _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
            _AddReceivedPayments = AddReceivedPayments.AddReceivedPayment(self.cookie, self.csrf)
            _AddContract = AddContract.AddContract(self.cookie, self.csrf)
            a = a + 1
            if userinfo['username'] == '13799999999' :
                self.add_data(a,DepartmentId = 0)
                self.add_data(a,DepartmentId = 1)
            else:
                self.add_data(a, DepartmentId=0)


    def add_data(self,a,DepartmentId):
        _ContractsApproval = ContractsApproval.Approvals(self.cookie, self.csrf)
        _ReceivedPaymentApproval = ReceivedPaymentApproval.Approvals(self.cookie, self.csrf)
        _AddReceivedPayments = AddReceivedPayments.AddReceivedPayment(self.cookie, self.csrf)
        _AddContract = AddContract.AddContract(self.cookie, self.csrf)
        #合同审批通过后，回款审批通过（P1-2）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId,approve_status='applying')
        _ContractsApproval.verify_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同审批通过后，回款审批否决（P1-3）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.verify_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同审批通过后，回款待审批（P1-4）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.verify_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * ( i + 1),customer_id=contract_return_id[1])
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])

        # 合同审批通过后，回款审批否决（P1-5）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')  # id[0]为合同id id[1]为客户id
        _ContractsApproval.verify_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录通过后驳回
            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(_AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])))
            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])))
        # 合同待审批，回款审批通过（P2-2）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))

        # 合同待审批，回款审批驳回（P2-3）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同待审批，回款待审批（P2-4）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        for i in range(6):
            # 添加新增回款记录
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0], receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])

        # 合同待审批，回款通过后驳回（P2-5）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')  # id[0]为合同id id[1]为客户id
        for i in range(6):
            # 添加新增回款记录通过后驳回
            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])))
            _ReceivedPaymentApproval.received_payments_deny(_ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])))

        # 合同否决，回款审批通过（P3-2）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.deny_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同否决，回款审批否决（P3-3）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.deny_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同否决，回款待审批（P3-4）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.deny_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])

        # 合同否决，回款通过后驳回（P3-5）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.deny_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录通过后驳回
            _ReceivedPaymentApproval.received_payments_deny(
                _ReceivedPaymentApproval.received_payments_verify(
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])))
            _ReceivedPaymentApproval.received_payments_deny(
                _ReceivedPaymentApproval.received_payments_verify(
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])))

        # 合同撤销，回款审批通过（P4-2）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.cancel_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_verify(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同撤销，回款审批否决（P4-3）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.cancel_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1]))
            _ReceivedPaymentApproval.received_payments_deny(
                _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                    amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1]))
        # 合同撤销，回款待审批（P4-4）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.cancel_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])
            _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])

        # 合同撤销，回款通过后驳回（P4-5）
        # 添加一个待审批的合同
        contract_return_id = _AddContract.add_contracts(DepartmentId=DepartmentId, approve_status='applying')
        _ContractsApproval.cancel_contracts(contract_return_id[0])
        for i in range(6):
            # 添加新增回款记录通过后驳回
            _ReceivedPaymentApproval.received_payments_deny(
                _ReceivedPaymentApproval.received_payments_verify(
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][0] * (i + 1),customer_id=contract_return_id[1])))
            _ReceivedPaymentApproval.received_payments_deny(
                _ReceivedPaymentApproval.received_payments_verify(
                    _AddReceivedPayments.add_received_payments(contract_id=contract_return_id[0],receive_date=self.sign_date_list[i],
                                                amount=self.total_amount_list[a - 1][1] * (i + 1),customer_id=contract_return_id[1])))

    def case_3(self):
        self.current_case = 'case 3'
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        print(self.userinfo_super['username'])
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
    _received_payment_amount =received_payment_amount()
    # os.remove('status_code_ok.txt')
    # # # os.remove('status_code.txt')
    # _received_payment_amount.case_3()
    # # #回款的case1
    # # # _received_payment_amount.case_1()
    # # # #回款的case2
    # _received_payment_amount.case_2()

# 按用户 回款金额  报表
#     _received_payments_amount_case1 = result_received_payments_amount_user_case1.result_received_payments_amount_user()
    # _received_payments_amount_case1.received_payments_amount_baobiao()
# # #按用户 回款金额 工作台
#     _received_payments_amount_case1.received_payments_amount_gongzuotai()
# 按部门 回款金额 报表
#     _received_payments_amount_d_case1 = result_received_payments_amount_department_case1.result_received_payments_amount_d()
#     _received_payments_amount_d_case1.payments_amount_baobiao()




# 按用户 回款金额  报表
    _received_payments_amount_case2 = result_received_payments_amount_user_case2.result_received_payments_amount_user()
# #     _received_payments_amount_case2.received_payments_amount_baobiao()
# # # #  #按用户 回款金额 工作台
    _received_payments_amount_case2.received_payments_amount_gongzuotai()
# # 按部门 回款金额 报表
#     _received_payments_amount_d_case2=result_received_payments_amount_department_case2.result_received_payments_amount_department()
# # #
#     _received_payments_amount_d_case2.received_payments_amount_d_baobiao()








