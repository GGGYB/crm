# -*- coding: utf-8 -*-
import datetime
import os
import codecs
import operator
from commons.const import const
from testCase.login import testLogin as login
from testCase.performance import result
import json



class result_win_count_month:
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

        self.title_list_first = [['用户按月查看1月商机数'],
                      ['用户按月查看第一季度商机数'],
                      ['用户按月查看本年商机数']
                      ]
        self.month = [[1], [3], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                      [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [4, 5, 6, 7, 8]]

        self.title = [['用户按月查看1月商机数'],
                      ['用户按月查看3月商机数'],
                      ['用户按月查看第一季度商机数'],
                      ['用户按月查看第二季度商机数'],
                      ['用户按月查看第三季度商机数'],
                      ['用户按月查看第四季度商机数'],
                      ['用户按月查看本年商机数'],
                      ['用户按月查看上半年商机数'],
                      ['用户按月1查看下半年商机数'],
                      ['用户按月查看4~8月商机数']
                      ]

        pass

#用户按月实际结果和预期结果对比
    def check_data_user(self,i =0):
        current_case = self.title[i]
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _result = result.result(self.cookie, self.csrf)
        # Actual_result输出三个值 图表，中间值，表格
        Actual_result_all = _result.gole(from_date=self.date_list[i][0],to_date=self.date_list[i][1],type = 'win_count',dimension ='user')
        # Expected_result输出两个值 中间值，表格
        Expected_result_all =_result.count_get_month_user(self.month[i])
        # 比较图表的统计值是否相同
        Actual_result = Actual_result_all[0]
        #图表的预期结果和表格的预期结果相同 所以取的是表格预期结果的值
        Expected_result = Expected_result_all[1]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case)+'图表的排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
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
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case)+'中间统计排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
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
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')

#工作台的对比
    def check_data_first(self,i=0):
        current_case = self.title_list_first[i]
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _result = result.result(self.cookie, self.csrf)
        # 只返回表格的排名
        Actual_result = _result.sales_rank(tpye="win_count", scope_unit=self.date_list_first[i][0])
        print('========')
        print(Actual_result)
        print('===========')
        # 返回中间的统计值,表格的排名
        Expected_result_all = _result.count_get_user(self.month_list_first[i])
        Expected_result=Expected_result_all[1]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            print(test_result)
            if test_result == True:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case)+'工作台对比' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('opportunities_number_month.txt', 'a', 'utf-8')
                a = str(str(current_case)+'工作台对比' + ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')

    # 用户按月结果对比
    def test_case(self):
        _result_count = result_win_count_month()
        s = len(_result_count.date_list)
        for i in range(s):
            _result_count.check_data_user(i)

    # 工作台结果对比
    def test_case2(self):
        _result_count = result_win_count_month()
        for i in range(len(self.month_list_first)):
            _result_count.check_data_first(i)

if __name__ == '__main__':
    _result_count =result_win_count_month()
    # os.remove('opportunities_number_month.txt')
    #工作台结果对比
    # _result_count.test_case2()
    #用户按月结果对比
    _result_count.test_case()
    #测试此方法
    # _result_count.check_data_user()
    #测试此方法
    # _result_count.check_data_first()



