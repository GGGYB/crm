# -*- coding: utf-8 -*-
__author__ = 'lwang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import codecs
# import MySQLdb
import re
from decimal import Decimal as D
from commons.const import const
from commons import common

class Login:
    def __init__(self):
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.uid =''
        self.csrf = ''
        self.cookie = ''
        self.role = ''
        self.username = ''
        self.password = ''
        self.response = ''
        self.csrf1 = ''
        self.given_cookie = ''  # 用于存储人工指定的cookie，一旦设置后，就不使用页面内获取的cookie
        self.authorization = ''
        self.lead_ids = []
        self.user_id = ''
        self.customers_id =[]
        self.customers_id1 = ''
        self.contracts_id = ''
        self.sql_host = 'rdscbq34656z0ix59br0.mysql.rds.aliyuncs.com'
        self.products_id = ''
        self.expense_id = ''
        self.expense_id_list = []
        self.expense_accounts_id = ''
        self.payment_id_list = []
        self.payslip_stats_list = []
        self.commission_rules_id = []
        self.performance_indicator_id  = ''
        self.stations_id = ''
        self.revisit_logs_list = []
        self.token = ''
        self.common = common.Common("cookie","csrf")
       # 某些post或是get时要求header里带的信息，应该是一个帐户对应于唯一一个
        # 格式类似于：'Token token=cb5e0c1db161fe92a7f4ce67754821, uid=b9d28be2d18075de7435'
        pass

    def get_csrf_and_cookie(self):
        response = requests.get(self.base_url)
        html_str = response.content
        soup = BeautifulSoup(html_str, 'html.parser')
        #<meta name="csrf-token" content="jSoItF5xtWY0xvgUR5iIk7uphiyHGuCcVrAY8hBci42WBHPSxABibG07sMc0aSdnODraUrZ14rfd2uFEytfy+Q==" />
        self.csrf = soup.find(attrs={"name": "csrf-token"})['content']
        self.cookie = response.headers['Set-Cookie']
        # print(self.cookie)

    def get_csrf_by_html(self, html_str):
        soup = BeautifulSoup(html_str, 'html.parser')
        #print u'wnagle%s' %soup
        csrf = soup.find(attrs={"name": "csrf-token"})['content']
        if len(csrf):
            self.csrf = csrf
            # print (self.csrf)

    def get_html(self, url, content):
        s = requests.session()
        if len(self.given_cookie):
            s.headers.update({'Cookie': self.given_cookie})
        else:
            s.headers.update({'Cookie': self.cookie})
        s.headers.update({'Accept': 'text/html, application/xhtml+xml'})
        s.headers.update({'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0'})
        s.headers.update({'X-CSRF-Token': self.csrf})
        response = s.get(url)
        success_str = u'%s， success， response time： %s' % (content, response.elapsed)
        fail_str = u'%s， error' % content
        if response.status_code not in [200, 204]:
            self.response = None
            # print fail_str
            # print u'status code： %s' % response.status_code
            return False
        else:
            if response.headers['Set-Cookie']:
                self.cookie = response.headers['Set-Cookie']
            self.response = response
            #每次刷新页面后，更新token
            self.get_csrf_by_html(response.text)
            return True

    def get_csrf_by_home_html(self):
        url = self.base_url
        success = self.get_html(url, 'get csrf by home html')
        return success

    def login(self, username, password,role):
        # print (self.base_url2)
        self.username = username
        self.password = password
        url = self.base_url2
        body = {
            'login': username,
            'password': password,
            'device':'web'
        }
        s = requests.session()
        s.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
        s.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        s.headers.update({'Accept-Encoding': 'gzip, deflate'})
        s.headers.update({'Accept-Language': 'zh-CN,zh;q=0.8'})
        s.headers.update({'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0'})
        s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'})
        s.headers.update({'Cookie': self.cookie})
        response = s.post(url=url, data=body)
        # print ('login response status code')
        self.token = (response.json()['data']['user_token'])
        if response.status_code == 200:
            print ('login success')
        else:
            print ('login error')
        f = codecs.open('status_code_ok.txt', 'a', 'utf-8')
        # print (username)
        a = str(self.common.get_today_str()) +" " +username +"role：" + role
        f.write(a + '\n')
        f.close()

        f = codecs.open('status_code.txt', 'a', 'utf-8')
        a = str(self.common.get_today_str()) +" "+username + "role：" + role
        f.write(a + '\n')
        f.close()
        self.cook_get_pc()
        self.get_csrf_by_home_html()

    def uc_login(self, username, password,role):
        url = self.base_url2 + 'login'
        body = {
            'noticeType': "all",
            'password': password,
            'phone': username,
            'type': "login"
        }
        s = requests.session()
        s.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
        s.headers.update({'Content-Type': 'application/json; charset=UTF-8'})
        s.headers.update({'Accept-Encoding': 'gzip, deflate'})
        s.headers.update({'Accept-Language': 'zh-CN,zh;q=0.8'})
        s.headers.update({'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0'})
        s.headers.update({'appToken': 'f6620ff6729345c8b6101174e695d0ab'})
        response = s.post(url=url,  data=json.dumps(body))
        if response.status_code == 200:
            print ('login success')
            self.uid  = response.json()['data']['uid']
            self.ticket = response.json()['data']['ticket']
            print(response.json())
        else:
            print ('login error')
        f = codecs.open('status_code_ok.txt', 'a', 'utf-8')
        print (self.ticket)
        a = str(self.common.get_today_str()) +" " +username +"role：" + role
        f.write(a + '\n')
        f.close()
        f = codecs.open('status_code.txt', 'a', 'utf-8')
        a = str(self.common.get_today_str()) +" "+username + "role：" + role
        f.write(a + '\n')
        f.close()
        self.cook_get()
        self.get_csrf_by_home_html()



    def uc_lixiao_login(self,uid):
        url = self.base_url2 + 'getAppUrls'
        body = {
            'noticeType': "other",
            'type': "login",
            'uid': uid
        }
        s = requests.session()
        s.headers.update({'Accept':'*/*'})
        s.headers.update({'Accept-Encoding':'gzip, deflate, br'})
        s.headers.update({'Accept-Language':'zh-CN,zh;q=0.9'})
        s.headers.update({'appToken': '9de95972d5c3455ba16a6cf8f4872dd4'})
        s.headers.update({'Connection':'keep-alive'})
        s.headers.update({'Content-Type':'application/json; charset=utf-8'})
        response = s.post(url = url,data = json.dumps(body))
        # print(response.json())
        print(response.status_code)
        print('login response status code')
        print(response.status_code)



    def AppUrls(self):
        url = self.base_url2+'getAppUrls'
        body = {
            'noticeType': "all",
            'type': "login",
            'uid': self.uid
        }
        appToken="f6620ff6729345c8b6101174e695d0ab",
        self.response = self.common.post_json_response_json(url, body,'get appurl')
        # print (self.response.json())

    def cook_get(self):
        url = self.base_url+'?st=%s' %self.ticket
        # print (url)
        body ={ }
        self.response = self.common.get_response_json(url, body,'get cookie')
        # print(response.status_code)
        # print (self.response)
        self.cookie =self.response.headers['Set-Cookie']
        # print (self.cookie)

    def cook_get_pc(self):
        url = self.base_url+'dingtalk/sessions/new?user_token=%s' %self.token
        # https: // ding - test.ikcrm.com / dingtalk / sessions / new?user_token = de9550e1a5d14950a1b41f35ee6c93b1
        # print (url)
        body ={ }
        self.response = self.common.get_response_json(url, body,'get cookie')
        # print(response.status_code)
        # print (self.response)
        self.cookie =self.response.headers['Set-Cookie']
        # print (self.cookie)

    def sign_out(self,username, password,role):
        if len(self.cookie) == 0:
            self.get_csrf_and_cookie()
        if len(self.cookie) == 0:
            print ('get csrf and cookie error')
            return
        self.username = username
        self.password = password
        url = self.base_url + 'users/sign_out'
        body = {
            '_method': 'delete',
            'authenticity_token': self.csrf,
        }
        s = requests.session()
        s.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
        s.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        s.headers.update({'Accept-Encoding': 'gzip, deflate'})
        s.headers.update({'Accept-Language': 'zh-CN,zh;q=0.8'})
        s.headers.update({'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0'})
        s.headers.update({'Cookie': self.cookie})
        response = s.post(url=url, data=body)
        print (response.status_code)
        print ('sign_out response status code')
        print (response.status_code)
        if response.status_code == 302:
            print ('sign_out success')
            self.cookie  = response.headers['Set-Cookie']
            #print self.cookie
        else:
            print ('sign_out error')
        f = codecs.open('status_code_ok.txt', 'a', 'utf-8')
        print (username)
        a = str(self.common.get_today_str()) +" " +username +"role：" + role
        f.write(a + '\n')
        f.close()

        f = codecs.open('status_code.txt', 'a', 'utf-8')
        a = str(self.common.get_today_str()) +" "+username + "role：" + role
        f.write(a + '\n')
        f.close()
        self.cook_get()
        self.get_csrf_by_home_html()


        # self.common.get_response_json(url, body, '当前用户退出')

    def  get_ticket(self,uid,role):
        url = 'https://uc-test.weiwenjia.com/api/script/skipWxLogin/getTiekct?uid=' + str(uid)
        body = { }
        response  = self.common.get_response_json(url,body,'get_ticket')
        self.ticket = response.json()['data']['ticket']
        # print(response.json())
        # print(response.json()['data']['ticket'])





if __name__ == "__main__":
    a_Login =Login()
    a_Login.login("13644446666","Ik123456","1234567")
    # a_Login.uc_login("18721277192","111111","1234567")
    # a_Login.AppUrls()
    # a_Login.cook_get()
    # a_Login.get_ticket()
    # a_Login.uc_lixiao_login('4500785')
