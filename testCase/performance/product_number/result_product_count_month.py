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



class result_product_count_month:
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
        self.title = 'case0按用户1查看上月产品销量'
        self.expected = ((['"设计部子部门-用户4"', '"产品部-用户3"', '"设计部-用户1"', '"主辅部门-用户6"', '"设计部-用户2"','"销售部-用户5"' ],
                          [ '1660.0','1060.0', '180.0', '6.0', '-20.0' , '-20.0']),
                          (['"设计部子部门-用户4"', '"设计部-用户1"', '"主辅部门-用户6"',  '"设计部-用户2"','"销售部-用户5"'],
                           [ '1660.0', '180.0', '6.0',  '-20.0','-20.0']),
                          (['"设计部-用户1"','"主辅部门-用户6"',  '"设计部-用户2"','"销售部-用户5"'],
                           ['180.0', '6.0',  '-20.0','-20.0']),
                          (['"设计部-用户1"', '"销售部-用户5"'],
                           ['180.0', '-20.0'])
                          )
        self.title1 = 'case1用户1按月查看1月产品销量'
        self.expected1 = ((['"2019一月"'],
                           ['42.0']),
                          (['"2019一月"'],
                           ['36.0']),
                          (['"2019一月"'],
                           ['28.0']),
                          (['"2019一月"'],
                           ['12.0'])
                          )

        self.title2 = 'case2用户1按月查看3月产品销量'
        self.expected2 = ((['"2019三月"'],
                           ['42.0']),
                          (['"2019三月"'],
                           ['36.0']),
                          (['"2019三月"'],
                           ['28.0']),
                          (['"2019三月"'],
                           ['12.0'])
                          )

        self.title3 = 'case3用户1按月查看上季度产品销量'
        self.expected3 = (['"设计部子部门-用户4"', '"产品部-用户3"', '"设计部-用户1"', '"主辅部门-用户6"', '"设计部-用户2"', '"销售部-用户5"'],
                          ['', '', '', '', '', ''])
        self.title4 = 'case4用户1按月查看1 2 3季度产品销量'
        self.expected4 = ((['"2019一月"', '"2019三月"'],
                           ['42.0', '42.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['36.0', '36.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['28.0', '28.0']),
                          (['"2019一月"', '"2019三月"'],
                           ['12.0', '12.0'])
                          )
        self.title5 = 'case5用户1按月查看4 5 6季度产品销量'
        self.expected5 = ((['"2019五月"'],
                           ['42.0']),
                          (['"2019五月"'],
                           ['36.0']),
                          (['"2019五月"'],
                           ['28.0']),
                          (['"2019五月"'],
                           ['12.0'])
                          )
        self.title6 = 'case6用户1按月查看本年产品销量'
        self.expected6 = ((['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['42.0', '42.0', '42.0', '42.0', '42.0', '42.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['36.0', '36.0', '36.0', '24.0', '24.0', '24.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['28.0', '28.0', '28.0', '16.0', '16.0', '16.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"', '"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['12.0', '12.0', '12.0', '12.0', '12.0', '12.0'])
                          )
        self.title7 = 'case7用户1按月查看上半年产品销量'
        self.expected7 = ((['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['42.0', '42.0', '42.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['36.0', '36.0', '36.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['28.0', '28.0', '28.0']),
                          (['"2019一月"', '"2019三月"', '"2019五月"'],
                           ['12.0', '12.0', '12.0'])
                          )
        self.title8 = 'case8用户1按月查看下半年产品销量'
        self.expected8 = ((['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['42.0', '42.0', '42.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['24.0', '24.0', '24.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['16.0', '16.0', '16.0']),
                          (['"2019七月"', '"2019九月"', '"2019十一月"'],
                           ['12.0', '12.0', '12.0'])
                          )
        self.title9 = 'case9用户1按月查看04--08产品销量'
        self.expected9 = ((['"2019五月"', '"2019七月"'],
                           ['42.0', '42.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['36.0', '24.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['28.0', '16.0']),
                          (['"2019五月"', '"2019七月"'],
                           ['12.0', '12.0'])
                          )
        self.title10 = 'case9用户1按月查看 7 8 9产品销量'
        self.expected10 = ((['"2019七月"', '"2019九月"'],
                            ['42.0', '42.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['24.0', '24.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['16.0', '16.0']),
                           (['"2019七月"', '"2019九月"'],
                            ['12.0', '12.0'])
                           )
        self.title11 = 'case9用户1按月查看10 11 12产品销量'
        self.expected11 = ((['"2019十一月"'],
                            ['42.0']),
                           (['"2019十一月"'],
                            ['24.0']),
                           (['"2019十一月"'],
                            ['16.0']),
                           (['"2019十一月"'],
                            ['12.0'])
                           )
        pass

    def case_1(self,title,expected,data1,data2,dimension1):
        #按用户查看1月产品销量
        self.current_case =title
        _Roles =testGetRoles.GetRole(self.cookie,self.csrf)
        list=['organization_own','self_and_subordinate_department_own','self_department_own','self_own']
        for i in range(4):
            _Roles.ding_set_data_authority(list[i])
            _result=result.result(self.cookie,self.csrf)
            Actual_result =_result.gole_quarter(data1,data2,type='product_count',dimension=dimension1)
            test_result=operator.eq(expected[i], Actual_result)
            print (test_result)
            if test_result== True:
                f = codecs.open('product_count_month.txt', 'a', 'utf-8')
                a = str(self.current_case + ': '  "is right "+str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('product_count_month.txt', 'a', 'utf-8')
                a = str(i)+str(self.current_case + ': '  "is wrong, expected_result:'\n'" + str(expected[i]) +"Actual_result:'\n'"+ str(Actual_result)+','+str(datetime.datetime.now()))
                f.write(a + '\n')

    def case_test(self):
        os.remove('product_count_month.txt')
        _login = login.Login()
        print (self.userinfo_super['username'])
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        # 1月----
        _result_amount.case_1(title=_result_amount.title1, expected=_result_amount.expected1,
                              data1=_result_amount.date_list[1][0], data2=_result_amount.date_list[1][1],
                              dimension1=_result_amount.dimension1)

        # # 3月
        _result_amount.case_1(title=_result_amount.title2, expected=_result_amount.expected2,
                              data1=_result_amount.date_list[2][0], data2=_result_amount.date_list[2][1],
                              dimension1=_result_amount.dimension1)
        # #
        # # # 上季度
        # # _result_amount.case_1(title=_result_amount.title3, expected=_result_amount.expected3,
        # #                       data1=_result_amount.date_list[3][0], data2=_result_amount.date_list[3][1],
        # #                       dimension1=_result_amount.dimension1)
        # #
        # # #1 2 3
        _result_amount.case_1(title=_result_amount.title4, expected=_result_amount.expected4,
                              data1=_result_amount.date_list[4][0], data2=_result_amount.date_list[4][1],
                              dimension1=_result_amount.dimension1)
        # #
        # # # 4 5 6
        _result_amount.case_1(title=_result_amount.title5, expected=_result_amount.expected5,
                              data1=_result_amount.date_list[5][0], data2=_result_amount.date_list[5][1],
                              dimension1=_result_amount.dimension1)
        # # #
        #
        # # # #本年
        _result_amount.case_1(title=_result_amount.title6, expected=_result_amount.expected6,
                              data1=_result_amount.date_list[6][0], data2=_result_amount.date_list[6][1],
                              dimension1=_result_amount.dimension1)
        # # #
        # # #上半年
        _result_amount.case_1(title=_result_amount.title7, expected=_result_amount.expected7,
                              data1=_result_amount.date_list[7][0], data2=_result_amount.date_list[7][1],
                              dimension1=_result_amount.dimension1)
        # #
        # # # #下半年
        _result_amount.case_1(title=_result_amount.title8, expected=_result_amount.expected8,
                              data1=_result_amount.date_list[8][0], data2=_result_amount.date_list[8][1],
                              dimension1=_result_amount.dimension1)

        # # # 2019-04-01--2019-08-31
        _result_amount.case_1(title=_result_amount.title9, expected=_result_amount.expected9,
                              data1=_result_amount.date_list[9][0], data2=_result_amount.date_list[9][1],
                              dimension1=_result_amount.dimension1)
        # # # # #
        # # # #7 8 9
        _result_amount.case_1(title=_result_amount.title10, expected=_result_amount.expected10,
                              data1=_result_amount.date_list[10][0], data2=_result_amount.date_list[10][1],
                              dimension1=_result_amount.dimension1)
        # # # # #
        # # # #10 11 12
        _result_amount.case_1(title=_result_amount.title11, expected=_result_amount.expected11,
                              data1=_result_amount.date_list[11][0], data2=_result_amount.date_list[11][1],
                              dimension1=_result_amount.dimension1)
        # # # # #


if __name__ == '__main__':
    _result_amount =result_product_count_month()
    # os.remove('contraces_amount.txt')
    _result_amount.case_test()
    # 上月
    # _result_amount.case_1(title=_result_amount.title,expected=_result_amount.expected,data1=_result_amount.date_list[0][0],data2=_result_amount.date_list[0][1],dimension1='user')


