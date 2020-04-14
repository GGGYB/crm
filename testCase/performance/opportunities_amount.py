import os
from commons.const import const
from testCase.login import testLogin as login
from testCase.opportunities import testSettingsOpportunityApproval as ApprovalOppo
from testCase.opportunities import testAddOpportunity as AddOppo
from testCase.opportunities import testDeleteOpportunity as DeleteOppo
from testCase.performance.result_opprtunities_amount import result_oppotunitites_amount
from testCase.performance.result_opprtunities_amount import result_oppotunitites_amount_departments

class opportunities_amount:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        # self.userinfo_super = {'username': '15639356523', 'password': 'Ab123456','role':'超管'}
        # self.sign_date_list = ['2019-01-31', '2019-03-31', '2019-05-31', '2019-07-31', '2019-09-30', '2019-11-30']
        # self.total_amount_list = [[110,-20],[210,-220],[310,220],[410,420],[510,-520],[1,2]]
        # self.userinfo_list = [
        #                     {'username': '13701649175', 'password': 'Ik123456', 'role': '1'}
        #                       ,{'username': '15639356589', 'password': 'Ik123456', 'role': '2'}
        #                       ,{'username': '15639356542', 'password': 'Ik123456', 'role': '3'},
        #                       {'username': '15639356581', 'password': 'Ik123456', 'role': '4'},
        #                       {'username': '15639354896', 'password': 'Ik123456', 'role': '5'},
        #                       {'username': '13660139206', 'password': 'Ik123456', 'role': '6'}
        # ]
        # stage = [268994, 268992, 268991, 268990, 268989, 308555, 308556, 308557, 3085558, 308559, 308560, 308561, '']
        #stage_win ='268993' 独立
        # 钉钉test
        self.stage = [222996, 222995, 222994, 222993, 222992, 222991, 222990, 308557, 3085558, 308559, 308560, 308561, '']
        self.stage_win ='222997'
        # 钉钉staging
        # stage = [199481, 199480, 199479, 199478, 199477, 199476, 199475, 308557, 3085558, 308559, 308560, 308561, '']
        # stage_win = '199481'
        self.userinfo_super = {'username': '18049905933', 'password': 'Ik123456','role':'超管'}
        self.sign_date_list = ['2019-01-31', '2019-03-31', '2019-05-31', '2019-07-31', '2019-09-30', '2019-11-30']
        self.total_amount_list = [[110, -20], [260, -220], [310, 220], [410, 420], [510, -520], [1, 2], [200, 100],
                                  [220, 230]]
        self.userinfo_list = const.USER
        pass

    def case_1(self):
        stage=self.stage
        stage_win =self.stage_win
        self.current_case = 'case 1'
        _login = login.Login()
        a = 0
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie =_login.cookie
        self.csrf = _login.csrf
        _ApprovalOppo =ApprovalOppo.Approvals(self.cookie,self.csrf)
        _ApprovalOppo.close_opportunitie_approval()

        for userinfo in self.userinfo_list:
            _login.login(userinfo['username'], userinfo['password'], userinfo['role'])
            self.cookie =_login.cookie
            self.csrf = _login.csrf
            _AddOppo = AddOppo.AddOpportunities(self.cookie,self.csrf)
            _ApprovalOppo =ApprovalOppo.Approvals(self.cookie,self.csrf)
            a= a+1
            for i in range(6):
                if userinfo['username'] == '13799999999' and i >= 3:
                # if userinfo['username'] == '13660139206' and i >= 3:
                    #添加商机审批关闭 268893为赢单
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1), stage=stage_win,DepartmentId=1)
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][1] * (i + 1), stage=stage_win,DepartmentId=1)
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a - 1][0] * (i + 1), stage=stage[i],DepartmentId=1)
                else:
                # 添加商机审批关闭 268893为赢单
                    _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),stage=stage_win)
                    _AddOppo.add_opportunities(sign_date=self.sign_date_list[i], total_amount=self.total_amount_list[a-1][1]*(i+1),stage=stage_win)
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
                # if userinfo['username'] == '13660139206' and i >= 3:
                    # 待审批的商机
                    _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1)

                    # 审批通过的商机
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][1]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i],DepartmentId=1))

                    # 审批通过后否决
                    oppo_id=_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1)
                    _ApprovalOppo.approve_opportunity(oppo_id)
                    _ApprovalOppo.deny_opportunities_approval(oppo_id)

                    # # 审批否决的商机
                    _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))

                    # # 商机撤销
                    _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win,DepartmentId=1))

                else:
                    # 待审批的商机
                    _AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win)

                    # 审批通过的商机
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][1]*(i+1),approve_status='applying',stage=stage_win))
                    _ApprovalOppo.approve_opportunity(_AddOppo.add_opportunities(sign_date=self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage[i]))

                    # 审批通过后否决
                    oppo_id=_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win)
                    _ApprovalOppo.approve_opportunity(oppo_id)
                    _ApprovalOppo.deny_opportunities_approval(oppo_id)

                    # # 审批否决的商机
                    _ApprovalOppo.deny_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))

                    # # 商机撤销
                    _ApprovalOppo.cancel_opportunities_approval(_AddOppo.add_opportunities(sign_date =self.sign_date_list[i],total_amount=self.total_amount_list[a-1][0]*(i+1),approve_status='applying',stage=stage_win))

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
    _opportunities_amount =opportunities_amount()
    os.remove('status_code_ok.txt')
    os.remove('status_code.txt')
    # _opportunities_amount.case_2()
    # _opportunities_amount.case_1()

    # 按用户   报表完成度排名商机金额筛选
    _result_amount = result_oppotunitites_amount.result_opportunities_amount()
    # 按用户 商机金额 报表的筛选
    # _result_amount.opportunities_amount_baobiao()
    # 按用户  商机金额  工作台 筛选
    _result_amount.opportunities_amount_gongzuotai()
    # 按部门  报表
    _result_amount = result_oppotunitites_amount_departments.result_opportunities_amount_departments()
    _result_amount.opportunities_amount_d_baobiao()











