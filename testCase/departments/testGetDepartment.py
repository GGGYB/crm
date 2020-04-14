# -*- coding:utf-8 -*-
__author__ = "chunli"
import re
from commons import common
from commons.const import const
from bs4 import BeautifulSoup

class GetDepartment:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.baseUrl = const.BASE_URL

    def getDepartmentId(self):
        url = self.baseUrl + 'contracts/new?event_name=crmListAdd'
        params = {

        }
        response = self.common.get_response_json(url, params, '获取用户的的部门')
        soup = BeautifulSoup(response.text, "html.parser")
        current_department = (str(soup).split('所属部门')[1])
        Department_list =[]
        current_department_list= re.findall(r'value=\'(.+?)\'', current_department)
        # print (str(current_department_list))
        for item in current_department_list:
            data = re.findall(r'(\d+)', item)
            # print(data)
            Department_list.append( ''.join(data))
        # print (Department_list)
        #钉钉test加上以下这一句话
        Department_list.sort(reverse=True)
        # print(Department_list)
        return Department_list

    # def get_data_list(a_list):
    #     result_list = []
    #     for item in a_list:
    #         data = re.findall(r'(\d+)', item)
    #         print(data)
    #         result_list += data
    #     return result_list
    #
    # print('-' * 20)
    # mn2 = re.findall(r'value=\'(.+?)\'', s)
    # data_list = get_data_list(mn2)
    # print(data_list)

