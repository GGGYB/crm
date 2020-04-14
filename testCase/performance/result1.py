from bs4 import BeautifulSoup
import re
from commons import common
from commons.const import const
from testCase.login import testLogin as login
from testCase.performance import result as result


class result_data:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = ''
        self.cookie = ''
        self.userlist = const.USER
        self.total_amount_list = [[110, -20], [260, -220], [310, 220], [410, 420], [510, -520], [1, 2], [200, 100],
                                  [220, 230]]
        self._months = [1, 3, 5, 7, 9, 11]
        self._username=[]
        self._user_department =[]
        # ['设计部-用户1', '设计部-用户2', '产品部-用户3', '设计部子部门-用户4', '销售部-用户5', '主辅部门-用户6', '同部门下属-用户7', '设计部二级部门-用户8']
        # ['销售部', '设计部二级部门', '设计部', '产品部', '设计部子部门']
        pass

    def user_info(self):
        _user_department1=[]
        for i in self.userlist:
            _usertitle = i['usertitle']
            self._username.append(_usertitle)
            department = i['departments'][0]
            _user_department1.append(department)
        # self._user_department = list(set(self._user_department))
        for i in _user_department1:
            if i not in self._user_department:
                self._user_department.append(i)
        print(self._username)
        print(self._user_department)

    def amount_get_department(self,_months=[1],_user_department = ['设计部']):
        self.user_info()
        month = [[1], [3], [1, 3], [5], [1, 3, 5], [7, 9, 11]]
        payments_amount_case2_list = result.result.payments_amount_get(self,s=8)
        for _months in month:
            for i in self._user_department:
                t = 0
                for payments_amount_case2 in payments_amount_case2_list:
                    if _months.__contains__(payments_amount_case2['month']) and payments_amount_case2[' user_department'] == i:
                    # if payments_amount_case2['month'] in (1,3) and payments_amount_case2[' user_department'] == i:
                        # if _months.__contains__(payments_amount_case2['month']) and _user_department.__contains__(payments_amount_case2[' user_department']):
                        a =payments_amount_case2['amount']
                        t = t+a
                print (t ,i,_months)

    def amount_get_user(self):
        self.user_info()
        month = [[1],[3],[1,3],[5],[1,3,5],[7,9,11]]
        payments_amount_case2_list = result.result.payments_amount_get(self, s=8)
        for _months in month:
            for i in self._username:
                t = 0
                for payments_amount_case2 in payments_amount_case2_list:
                    if _months.__contains__(payments_amount_case2['month']) and payments_amount_case2[' user_name'] == i:
                        # if payments_amount_case2['month'] in (1,3) and payments_amount_case2[' user_department'] == i:
                        # if _months.__contains__(payments_amount_case2['month']) and _user_department.__contains__(payments_amount_case2[' user_department']):
                        a = payments_amount_case2['amount']
                        t = t + a
                print(t, i,_months)


        # print([payments_amount_case2 for payments_amount_case2 in nested if _months.__contains__(payments_amount_case2['month']) and payments_amount_case2[' user_department'] =="设计部"])

    def count_get_department(self,_months=[1],_user_department = ['设计部']):
        self.user_info()
        month = [[1], [3], [1, 3], [5], [1, 3, 5], [7, 9, 11]]
        count_get_list = result.result.count_get(self)
        for _months in month:
            for i in self._user_department:
                c = 0
                for count_get in count_get_list:
                    if _months.__contains__(count_get['month']) and count_get[' user_department'] == i:
                        # print (count_get)
                    # if payments_amount_case2['month'] in (1,3) and payments_amount_case2[' user_department'] == i:
                        # if _months.__contains__(payments_amount_case2['month']) and _user_department.__contains__(payments_amount_case2[' user_department']):
                        a =count_get['count']
                        # print (a)
                        c = c+a
                print (c ,i,_months)

    def count_get_user(self,_months=[1,3,5],_user_department = ['设计部']):
        self.user_info()
        count_get_list = result.result.count_get(self)
        result_count =[]
        for i in self._username:
            c = 0
            for count_get in count_get_list:
                if _months.__contains__(count_get['month']) and count_get[' user_name'] == i:
                    a =count_get['count']
                    c = c+a
            print (c ,i,_months)
            count_info = {
                'month': _months,
                'count': float(c),
                ' user_name': i,
            }
            result_count.append(count_info)
        print (result_count)
        result_count = sorted(result_count, key=lambda item: item['count'], reverse=True)
        print (result_count)








if __name__ == '__main__':
    _result_data =result_data()
    # os.remove('status_code_ok.txt')
    # os.remove('status_code.txt')
    # _result_data.amount_get_department()
    # _result_data.amount_get_user()
    # _result_data.count_get_department()
    _result_data.count_get_user()
    # _contracts_amount.gole()