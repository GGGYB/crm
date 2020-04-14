# -*- coding: utf-8 -*-
import datetime
import os
import codecs
import operator
from commons.const import const
from testCase.login import testLogin as login
from testCase.performance import result
import json



class result_product_category_number_departments:
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

        self.month = [[1], [3], [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                      [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [4, 5, 6, 7, 8]]

        self.title = [['按部门查看1月产品分类销量数'],
                      ['按部门查看3月产品分类销量数'],
                      ['按部门查看第一季度产品分类销量数'],
                      ['按部门查看第二季度产品分类销量数'],
                      ['按部门查看第三季度产品分类销量数'],
                      ['按部门查看第四季度产品分类销量数'],
                      ['按部门查看本年产品分类销量数'],
                      ['按部门查看上半年产品分类销量数'],
                      ['按部门1查看下半年产品分类销量数'],
                      ['按部门查看4~8月产品分类销量数']
                      ]

        pass

#按部门实际结果和预期结果对比
    def check_data_department(self,i =0):
        current_case = self.title[i]
        _login = login.Login()
        _login.login(self.userinfo_super['username'], self.userinfo_super['password'], self.userinfo_super['role'])
        self.cookie = _login.cookie
        self.csrf = _login.csrf
        _result = result.result(self.cookie, self.csrf)
        # Actual_result输出三个值 图表，中间值，表格
        Actual_result_all = _result.gole_d(from_date=self.date_list[i][0],to_date=self.date_list[i][1],type = 'product_category_count',dimension ='department')
        # Expected_result输出两个值 中间值，表格
        Expected_result_all =_result.count_get_department(self.month[i],s=4)

        # 比较图表的统计值是否相同
        Actual_result = Actual_result_all[0]
        #图表的预期结果和表格的预期结果相同 所以取的是表格预期结果的值
        Expected_result = Expected_result_all[1]

        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True:
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a =str(i)+ str(str(current_case)+'图表的排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a = str(i)+str(str(current_case)+'图表的排名' + ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')
        #
        #比较实际中间的统计值和预期中间的统计值是否相同
        Actual_result=Actual_result_all[1]
        Expected_result=Expected_result_all[0]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True :
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a = str(str(current_case)+'中间统计排名' + ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a = str(str(current_case)+'中间统计排名' + ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(datetime.datetime.now()))
                f.write(a + '\n')
        #
        #比较表格的是否相等
        Actual_result = Actual_result_all[2]
        Expected_result = Expected_result_all[1]
        s = len(Actual_result)
        for i in range(s):
            test_result = operator.eq(Expected_result[i], Actual_result[i])
            if test_result == True:
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is right " + str(datetime.datetime.now()))
                f.write(a + '\n')
            else:
                f = codecs.open('product_category_count_d.txt', 'a', 'utf-8')
                a = str(str(current_case) +'表格排名'+ ': '  "is wrong, expected_result:'\n'" + str(
                    Expected_result[i]) + "Actual_result:'\n'" + str(Actual_result[i]) + ',' + str(
                    datetime.datetime.now()))
                f.write(a + '\n')


    # 按部门的用例
    def product_category_number_d_baobiao(self):
        s = len(self.date_list)
        for i in range(s):
            self.check_data_department(i)



if __name__ == '__main__':
    _result_count =result_product_category_number_departments()
    # os.remove('product_category_count_d.txt')
    #按部门结果对比
    _result_count.product_category_number_d_baobiao()
    #测试此方法
    # _result_count.check_data_user()



