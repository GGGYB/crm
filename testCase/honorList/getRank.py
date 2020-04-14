# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import re
from decimal import Decimal as D
from commons import common
from commons.const import const



class getRank:
    def __init__(self, cookie, csrf):
        #'https://e.ikcrm.com/
        # self.base_url = base_url
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        pass

    def get_rank(self):
        rank_type = ['contract_amount' , 'contract_payment_amount' , 'contract_count' , 'add_customer_count' , 'revisit_customer_count' ,'checkin_customer_count']
        date_type = ['yesterday' , 'today' , 'prev_week' , 'week' , 'last_month' ,'month' ,'quarter' , 'last_quarter' , 'year' , 'last_year']
        for i in range(len(date_type)):
            for j in range(len(rank_type)):
                # self.get_rank_by_dep(rank_type[j], date_type[i])
                self.get_rank_by_user(rank_type[j], date_type[i])




    def get_rank_by_dep(self,rank_type,date_type):
        url = self.base_url + 'api/dashboard/department_rank?rank_type=' + rank_type + '&date_type=' + date_type
        body = {}
        response  =  self.common.get_response_json(url , body ,'get_page')
        rank = []
        department = []
        count_or_amount = []
        for i in range(len(response.json()['rank'])):
            rank.append(response.json()['rank'][i]['ranking'])
            department.append(response.json()['rank'][i]['department_name'])
            count_or_amount.append(response.json()['rank'][i]['count_or_amount'])
        actual_dep_rank = []
        for i in range(len(rank)):
            dep_rank = {
                'date_type': date_type,
                'rank_type' : rank_type,
                'dep':department[i],
                ' rank': rank[i],
                'count_or_amount': count_or_amount[i]
            }
            actual_dep_rank.append(dep_rank)
        print(actual_dep_rank)

    def get_rank_by_user(self,rank_type,date_type):
        url = self.base_url + 'api/dashboard/user_rank?rank_type=' + rank_type + '&date_type=' + date_type
        body = {}
        response  =  self.common.get_response_json(url , body ,'get_page')
        rank = []
        user = []
        count_or_amount = []
        for i in range(len(response.json()['rank'])):
            rank.append(response.json()['rank'][i]['ranking'])
            user.append(response.json()['rank'][i]['user_name'])
            count_or_amount.append(response.json()['rank'][i]['count_or_amount'])
        actual_user_rank = []
        for i in range(len(rank)):
            user_rank = {
                'date_type': date_type,
                'rank_type' : rank_type,
                'dep':user[i],
                ' rank': rank[i],
                'count_or_amount': count_or_amount[i]
            }
            actual_user_rank.append(user_rank)
        print(actual_user_rank)
