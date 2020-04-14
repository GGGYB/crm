import datetime
import os
import codecs
import operator
from commons.const import const
from testCase.roles import testGetRoles
from commons import filters
from testCase.login import testLogin as login
from testCase.performance import result
from testCase.contracts import testContract as contracts
from testCase.contracts import testSettingsContractsApproval as ContractsApproval
from testCase.contracts import testAddContract as AddContract
from testCase.contracts import testDeleteContract as DeleteContract



class result_product_money_month:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        self.dimension1 = 'month'
        # self.dimension2 = 'department'
        self.userinfo_super = {'username': '15000249334', 'password': 'Ik123456','role':'超管'}
        # 上月 1月 3月 上季度 本季度 下季度 本年 上半年 下半年 第三季度  第四季度
        self.date_list = [['2018-12-01','2018-12-31'],['2019-01-01','2019-01-31'],['2019-03-01','2019-03-31'],['2018-10-01','2018-12-31'],['2019-01-01','2019-03-31'],['2019-04-01','2019-06-30'],['2019-01-1','2019-12-31'],['2019-01-01','2019-06-30'],['2019-07-01','2019-12-31'],['2019-04-01','2019-08-31'],['2019-07-01','2019-09-30'],['2019-10-01','2019-12-31']]
        self.title = 'case0用户1查看上月产品1的销售额'
        self.expected = ((['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"','"2019十一月"'],
                          [ '27300.0','54600.0', '81900.0', '109200.0', '136500.0' , '163800.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"','"2019十一月"'],
                           [ '24600.0','49200.0', '73800.0', '55200.0',  '69000.0','82800.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"','"2019十一月"'],
                           ['19800.0', '39600.0','54900.0', '36000.0',  '45000.0','54000.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"','"2019十一月"'],
                           ['300.0', '600.0','900.0', '1200.0','1500.0', '1800.0'])
                          )
        self.title1 = 'case1用户1查看1月产品1的销售额'
        self.expected1 = ((['"2019一月"'],
                           ['27300.0']),
                          (['"2019一月"'],
                           ['24600.0']),
                          (['"2019一月"'],
                           ['19800.0']),
                          (['"2019一月"'],
                           ['7800.0'])
                          )

        self.title2 = 'case2用户1查看3月产品1的销售额'
        self.expected2 = ((['"2019三月"'],
                           ['54600.0']),
                          (['"2019三月"'],
                           ['49200.0']),
                          (['"2019三月"'],
                           ['39600.0']),
                          (['"2019三月"'],
                           ['15600.0'])
                          )

        self.title3 = 'case3用户1查看上季度产品1的销售额'
        self.expected3 = (['"设计部子部门-用户4"', '"产品部-用户3"', '"设计部-用户1"', '"主辅部门-用户6"', '"设计部-用户2"', '"销售部-用户5"'],
                          ['', '', '', '', '', ''])
        self.title4 = 'case4用户1查看1 2 3季度产品1的销售额'
        self.expected4 = ((['"2019一月"', '"2019三月"'],
                           ['27300.0', '54600.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['24600.0', '49200.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['19800.0', '39600.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['7800.0', '15600.0'])
                          )
        self.title5 = 'case5用户1查看4 5 6季度产品1的销售额'
        self.expected5 = ((['"2019五月"'],
                           ['81900.0']),
                          (['"2019五月"'],
                           ['73800.0']),
                          (['"2019五月"'],
                           ['59400.0']),
                          (['"2019五月"'],
                           ['23400.0'])
                          )
        self.title6 = 'case6用户1查看本年产品1的销售额'
        self.expected6 = ((['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['27300.0', '54600.0', '81900.0', '109200.0', '136500.0', '163800.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['24600.0', '49200.0', '73800.0', '55200.0', '69000.0', '82800.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['19800.0', '39600.0', '59400.0', '36000.0', '45000.0', '54000.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['7800.0', '15600.0', '23400.0', '31200.0', '39000.0', '46800.0'])
                          )
        self.title7 = 'case7用户1查看上半年产品1的销售额'
        self.expected7 = ((['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['27300.0', '54600.0', '81900.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['24600.0', '49200.0', '73800.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['19800.0', '39600.0', '59400.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['7800.0', '15600.0', '23400.0'])
                          )
        self.title8 = 'case8用户1查看下半年产品1的销售额'
        self.expected8 = ((['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['109200.0', '136500.0', '163800.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['55200.0', '69000.0', '82800.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['36000.0', '45000.0', '54000.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['31200.0', '39000.0', '46800.0'])
                          )
        self.title9 = 'case9用户1查看04--08产品1的销售额'
        self.expected9 = ((['"2019五月"', '"2019七月"'],
                           ['81900.0', '109200.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['73800.0', '55200.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['59400.0', '36000.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['23400.0', '31200.0'])
                          )
        self.title10 = 'case9用户1查看 7 8 9产品1的销售额'
        self.expected10 = ((['"2019七月"', '"2019九月"'],
                            ['109200.0', '136500.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['55200.0', '69000.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['36000.0', '45000.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['31200.0', '39000.0'])
                           )
        self.title11 = 'case9用户1查看10 11 12产品1的销售额'
        self.expected11 = ((['"2019十一月"'],
                            ['163800.0']),
                           (['"2019十一月"'],
                            ['82800.0']),
                           (['"2019十一月"'],
                            ['54000.0']),
                           (['"2019十一月"'],
                            ['46800.0'])
                           )
        pass

    def case_1(self,title,expected,data1,data2,dimension1):
        #按用户查看1月产品1的销售额
        self.current_case =title
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _Roles =testGetRoles.GetRole(self.cookie,self.csrf)
        list=['organization_own','self_and_subordinate_department_own','self_department_own','self_own']
        for i in range(4):
            _Roles.ding_set_data_authority(list[i])
            # print('==========')
            # print (expected[i])
            # print ('============')
            _result=result.result(self.cookie,self.csrf)
            Actual_result =_result.gole_quarter(data1,data2,type='product_money',dimension=dimension1)
            # print (Actual_result)
            test_result=operator.eq(expected[i], Actual_result)
            print (test_result)
            if test_result== True:
                f = codecs.open('product_money_month.txt', 'a', 'utf-8')
                a = str(self.current_case + ': '  "is right "+str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('product_money_month.txt', 'a', 'utf-8')
                a = str(i)+str(self.current_case + ': '  "is wrong, expected_result:'\n'" + str(expected[i]) +"Actual_result:'\n'"+ str(Actual_result)+','+str(datetime.datetime.now()))
                f.write(a + '\n')

if __name__ == '__main__':
    _result_amount =result_product_money_month()
    # os.remove('product_money_month.txt')
    # 上月
    # _result_amount.case_1(title=_result_amount.title,expected=_result_amount.expected,data1=_result_amount.date_list[0][0],data2=_result_amount.date_list[0][1],dimension1='user')
    #1月----
    # _result_amount.case_1(title=_result_amount.title1, expected=_result_amount.expected1,
    #                      data1=_result_amount.date_list[1][0], data2=_result_amount.date_list[1][1], dimension1=_result_amount.dimension1)
    #
    # # # 3月
    # _result_amount.case_1(title=_result_amount.title2, expected=_result_amount.expected2,
    #                       data1=_result_amount.date_list[2][0], data2=_result_amount.date_list[2][1],
    #                       dimension1=_result_amount.dimension1)
    # # #
    # # # # 上季度
    # # # _result_amount.case_1(title=_result_amount.title3, expected=_result_amount.expected3,
    # # #                       data1=_result_amount.date_list[3][0], data2=_result_amount.date_list[3][1],
    # # #                       dimension1=_result_amount.dimension1)
    # # #
    # # # #1 2 3
    # _result_amount.case_1(title=_result_amount.title4, expected=_result_amount.expected4,
    #                       data1=_result_amount.date_list[4][0], data2=_result_amount.date_list[4][1],
    #                       dimension1=_result_amount.dimension1)
    # # #
    # # # # 4 5 6
    # _result_amount.case_1(title=_result_amount.title5, expected=_result_amount.expected5,
    #                       data1=_result_amount.date_list[5][0], data2=_result_amount.date_list[5][1],
    #                       dimension1=_result_amount.dimension1)
    # # #
    #
    # # # #本年
    _result_amount.case_1(title=_result_amount.title6, expected=_result_amount.expected6,
                          data1=_result_amount.date_list[6][0], data2=_result_amount.date_list[6][1],
                          dimension1=_result_amount.dimension1)
    # # #
    # # # #上半年
    # _result_amount.case_1(title=_result_amount.title7, expected=_result_amount.expected7,
    #                       data1=_result_amount.date_list[7][0], data2=_result_amount.date_list[7][1],
    #                       dimension1=_result_amount.dimension1)
    # # #
    # # # # #下半年
    # _result_amount.case_1(title=_result_amount.title8, expected=_result_amount.expected8,
    #                       data1=_result_amount.date_list[8][0], data2=_result_amount.date_list[8][1],
    #                       dimension1=_result_amount.dimension1)
    #
    # # # # 2019-04-01--2019-08-31
    # _result_amount.case_1(title=_result_amount.title9, expected=_result_amount.expected9,
    #                       data1=_result_amount.date_list[9][0], data2=_result_amount.date_list[9][1],
    #                       dimension1=_result_amount.dimension1)
    # # # # # #
    # # # # #7 8 9
    # _result_amount.case_1(title=_result_amount.title10, expected=_result_amount.expected10,
    #                       data1=_result_amount.date_list[10][0], data2=_result_amount.date_list[10][1],
    #                       dimension1=_result_amount.dimension1)
    # # # # # #
    # # # # #10 11 12
    # _result_amount.case_1(title=_result_amount.title11, expected=_result_amount.expected11,
    #                       data1=_result_amount.date_list[11][0], data2=_result_amount.date_list[11][1],
    #                       dimension1=_result_amount.dimension1)
    # # # # #

