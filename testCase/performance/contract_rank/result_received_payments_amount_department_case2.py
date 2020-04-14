# -*- coding: utf-8 -*-
import datetime
import os
import codecs
import operator
from commons.const import const
from testCase.login import testLogin as login
from testCase.performance import result
import json



class result_received_payments_amount_department:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        self.dimension1 = 'user'
        self.dimension2 = 'department'
        self.Actual_result =""
        self.userinfo_super = {'username': '18049905933', 'password': 'Ik123456','role':'超管'}

        self.date_list = [['2019-01-01', '2019-01-31'],
                          ['2019-03-01', '2019-03-31'],
                          ['2019-01-01', '2019-03-31'],
                          ['2019-04-01', '2019-06-30'],
                          ['2019-07-01', '2019-09-30'],
                          ['2019-10-01', '2019-12-31'],
                          ['2019-01-1', '2019-12-31'],
                          ['2019-01-01', '2019-06-30'],
                          ['2019-07-01', '2019-12-31'],
                          ['2019-04-01', '2019-08-31']]


        self.date_list_first = [
                          ['last_month'],
                          ['quarter'],
                          ['year']
                         ]

        self.month_list_first = [
                          [1],
                          [1, 2, 3],
                          [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                         ]

        self.title_list_first = [['按部门查看1月回款金额'],
                      ['按部门查看第一季度回款金额'],
                      ['按部门查看本年回款金额']
                      ]
        self.month = [[1], [3], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                      [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [4, 5, 6, 7, 8]]

        self.title = [['按部门查看1月回款金额'],
                      ['按部门查看3月回款金额'],
                      ['按部门查看第一季度回款金额'],
                      ['按部门查看第二季度回款金额'],
                      ['按部门查看第三季度回款金额'],
                      ['按部门查看第四季度回款金额'],
                      ['按部门查看本年回款金额'],
                      ['按部门查看上半年回款金额'],
                      ['按部门1查看下半年回款金额'],
                      ['按部门查看4~8月回款金额']
                      ]

        pass

#按部门实际结果和预期结果对比
    def check_data_user(self,i =0):
        current_case = self.title[i]
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _result = result.result(self.cookie, self.csrf)
        # Actual_result输出三个值 图表，中间值，表格
        Actual_result_all = _result.gole_department(from_date=self.date_list[i][0],to_date=self.date_list[i][1],type = 'contract_rank',dimension ='department')
        # Expected_result输出两个值 中间值，表格
        Expected_result_all =_result.payments_amount_get_department_case2(self.month[i])
        # 比较图表的统计值是否相同
        Actual_result = Actual_result_all[0]
        #图表的预期结果和表格的预期结果相同 所以取的是表格预期结果的值
        Expected_result = Expected_result_all[1]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True:
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case)+'图表的排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case)+'图表的排名' + ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')

        #比较实际中间的统计值和预期中间的统计值是否相同
        Actual_result=Actual_result_all[1]
        Expected_result=Expected_result_all[0]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True :
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case)+'中间统计排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case)+'中间统计排名' + ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(datetime.datetime.now()))
                f.write(a + '\n')

        #比较表格实际排名和预期排名是否相等
        Actual_result = Actual_result_all[2]
        Expected_result = Expected_result_all[1]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True:
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('contract_rank_d_case2.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')


    # 按部门结果对比
    def received_payments_amount_d_baobiao(self):
        _result_count = result_received_payments_amount_department()
        s = len(_result_count.date_list)
        for i in range(s):
            _result_count.check_data_user(i)


if __name__ == '__main__':
    _result_count =result_received_payments_amount_department()
    # os.remove('contract_rank_d_case2.txt')
    #工作台结果对比
    # _result_count.received_payments_amount_gongzuotai()
    #按部门结果对比
    _result_count.received_payments_amount_d_baobiao()
    #测试此方法
    # _result_count.check_data_user()
    #测试此方法
    # _result_count.check_data_first()



