import os
from commons.const import const
from testCase.login import testLogin as login
from testCase.opportunities import testSettingsOpportunityApproval as ApprovalOppo
from testCase.opportunities import testAddOpportunity as AddOppo
from testCase.opportunities import testDeleteOpportunity as DeleteOppo
from testCase.performance.result_opportunities_number import opportunities_number_user
from testCase.performance.result_opportunities_number import result_opportunities_number_departments


class opportunities_number:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        self.userinfo_super = {'username': '18049905933', 'password': 'Ik123456', 'role': '超管'}
        self.sign_date_list = ['2019-01-31', '2019-03-31', '2019-05-31', '2019-07-31', '2019-09-30', '2019-11-30']
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
        _ApprovalOppo =ApprovalOppo.Approvals(self.cookie,self.csrf)
        _ApprovalOppo.close_opportunitie_approval()
        # #独立
        # # stage = [268994, 268992, 268991, 268990, 268989, 308555, 308556, 308557, 3085558, 308559, 308560, 308561, '']
        # 钉钉test
        stage = [222996, 222995, 222994, 222993, 222992, 222991, 222990, 308557, 3085558, 308559, 308560, 308561, '']
        stage_win = '222997'
        #钉钉staging
        # stage = [199480, 199479, 199478, 199477, 199476, 199475, 308557, 3085558, 308559, 308560, 308561, '']
        # stage_win = '199481'
        a =0
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            print (userinfo['username'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _AddOppo = AddOppo.AddOpportunities(self.cookie,self.csrf)
            _ApprovalOppo =ApprovalOppo.Approvals(self.cookie,self.csrf)
            a= a+1
            for i in range(6):
                if userinfo['username'] == '13799999999' and i >= 3:
                    for b in range(a):
                    #添加商机审批关闭 268893为赢单
                        _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1), stage=stage_win,DepartmentId=1)
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1), stage=stage[i],DepartmentId=1)
                else:
                    for b in range(a):
                    # 添加商机审批关闭 268893为赢单
                        _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),stage=stage_win)
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1), stage=stage[i])


        _login.login(self.userinfo_super['username'], self.userinfo_super['password'],self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _ApprovalOppo = ApprovalOppo.Approvals(self.cookie, self.csrf)
        _ApprovalOppo.open_opportunitie_approval()
        a = 0
        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _AddOppo = AddOppo.AddOpportunities(self.cookie, self.csrf)
            _ApprovalOppo = ApprovalOppo.Approvals(self.cookie, self.csrf)
            a= a+1
            for i in range(6):
                    if userinfo['username'] == '13799999999' and i >= 3:
                        # 待审批的商机
                        _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1)
                        _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i+1), approve_status='applying',stage=stage[i],DepartmentId=1)
                        for b in range(a):
                        # 审批通过的商机
                            _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))
                        _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i],DepartmentId=1))
    #
                        # 审批通过后否决
                        oppo_id=_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1)
                        _ApprovalOppo.approve_opportunity(oppo_id)
                        _ApprovalOppo.deny_opportunities_approval(oppo_id)

                        # 审批通过后否决
                        oppo_id = _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],
                                                             total_amount=self.total_amount_list[a - 1][0] * (i + 1),
                                                             approve_status='applying', stage=stage[i], DepartmentId=1)
                        _ApprovalOppo.approve_opportunity(oppo_id)
                        _ApprovalOppo.deny_opportunities_approval(oppo_id)


                        # # 审批否决的商机
                        _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))
                        _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i],DepartmentId=1))

                        # # 商机撤销
                        _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))
                        _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i],DepartmentId=1))

                    else:
                        # 待审批的商机
                        _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win)
                        _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i+1), approve_status='applying',stage=stage[i])
                        for b in range(a):
                            # 审批通过的商机
                            _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))
                        _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i]))
    #
                        # 审批通过后否决
                        oppo_id=_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win)
                        _ApprovalOppo.approve_opportunity(oppo_id)
                        _ApprovalOppo.deny_opportunities_approval(oppo_id)

                        oppo_id = _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1),
                                                             approve_status='applying', stage=stage[i])
                        _ApprovalOppo.approve_opportunity(oppo_id)
                        _ApprovalOppo.deny_opportunities_approval(oppo_id)

                        # # 审批否决的商机
                        _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))
                        _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i]))

                        # # 商机撤销
                        _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))
                        _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i]))
    # #
    def case_2(self):
        self.current_case = 'case 2'
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie =_login.cookie
        self.csrf = _login.csrf
        _ApprovalOppo =ApprovalOppo.Approvals(self.cookie,self.csrf)
        _ApprovalOppo.close_opportunitie_approval()
        _DeleteOppo=DeleteOppo.DeleteOpportunities(self.cookie, self.csrf)
        b =_DeleteOppo.get_opportunitie_ids()
        print (b)
        page =b[0][0]
        print (page)
        for i in range(int(page)):
             c =_DeleteOppo.get_opportunitie_ids()
             oppo_list = c[1]
             for opportunitie_id in oppo_list:
                 _DeleteOppo.delete_opportunitie(opportunitie_id)




if __name__ == '__main__':
    _opportunities_number =opportunities_number()
    # os.remove('status_code_ok.txt')
    # os.remove('status_code.txt')
    # _opportunities_number.case_2()
    # _opportunities_number.case_1()

    #完成度排名商机数筛选
    _result_count = opportunities_number_user.result_opportunities_number_user()
    # 按用户 商机数 报表
    _result_count.opportunities_number_baobiao()
    # 按用户 商机数 工作台
    _result_count.opportunities_number_gongzuotai()
    # 按部门 商机数 报表
    _result_count = result_opportunities_number_departments.result_opportunities_number_departments()
    _result_count.opportunities_number_d_baobiao()










