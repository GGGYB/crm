# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
# from .testAddCustomer import AddCustomer


class UpdateOpportunities:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.users_id = []
        self.opportunities_id = []

    def testAdd(self):
        opportunity_id = self.add.add_opportunities()
        self.quick_edit_opportunitie(opportunity_id)
        self.upload_attachment_for_current_opportunity(opportunity_id)

    def update_opportunities_by_scope(self, scope, opportunities_id):
        self.quick_edit_opportunities(scope, opportunities_id)
        self.opportunities_field_update(scope, opportunities_id)
        # 批量转移商机
        self.opportunities_mass_transfer(scope, opportunities_id)
        # 批量添加协作人
        self.opportunities_add_assist_user(scope, opportunities_id)
        for opportunity_id in opportunities_id:
            self.add_assist_user_for_opportunitie(opportunity_id)
            self.upload_attachment_for_current_opportunity(opportunity_id)
            event_id = self.create_event_for_opportunitie(opportunity_id)
            self.update_event_complete(event_id)
            self.update_event_todo(event_id)
            self.get_event_todo(opportunity_id)

    # 批量编辑
    def opportunities_field_update(self, scope, opportunity_ids):
        url = self.base_url + 'batch_edit/field_form?model=Opportunity'
        # url = self.base_url + 'opportunities?scope=all_own&per_page=10&type=advance&section_only=true'
        params = {
            'model': 'opportunity'
        }
        response = self.common.get_response_json(url, params, '打开编辑商机的窗口')
        if response != False:
            S = response.content
            soup = BeautifulSoup(S, 'html.parser')
            optional_field = soup.find(attrs={'id': 'field_choice'})
            fields = re.findall(r"value=\"(.*?)\">", str(optional_field))
            # print (fields)
            selected_fields = soup.findAll(attrs={'class': 'batch-edit-custom-field hidden'})
            selected_field_list = []
            for i in selected_fields:
                selected_field = re.findall(r"value=\"(.*?)\">", str(i))
                selected_field_list.append(selected_field)
            # print(selected_field_list)
            url = self.base_url + 'api/opportunities/batch_update'
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'field_choice': fields[2],
                'opportunitie[' + fields[2] + ']': selected_field_list[1][3],
                'ids[]': opportunity_ids[0],
                'ids[]': opportunity_ids[1]
            }
            response = self.common.put_response_json(url, body, '批量编辑商机')
            return response

    # 快捷编辑商机
    def quick_edit_opportunities(self, scope, opportunity_ids):
        for opportunity_id in opportunity_ids:
            self.quick_edit_opportunitie('111111111', opportunity_id)

    # 快捷编辑单个商机
    def quick_edit_opportunitie(self, new_value, opportunity_id):
        url = self.base_url + 'quick_edit/field_form'
        params = {
            'model': 'opportunitie',
            'id': opportunity_id,
            'field_name': 'name',
            'page_type': 'index'
        }
        self.common.get_response_json(url, params, '获取商机详情sally***************')

        url = self.base_url + 'api/opportunities/' + str(opportunity_id)
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'opportunitie[id]': opportunity_id,
            'common_id': '',
            'opportunitie[name]': new_value
        }
        response = self.common.put_response_json(url, body, '快捷编辑商机，编辑的字段是：')
        if not response:
            return {}
        self.response = response
        return self.response.json()
    # 批量转移商机
    def opportunities_mass_transfer(self, scope, opportunities_id):
        url = self.base_url + 'api/opportunities/mass_transfer'
        self.users_id = self.users_get_all()
        body = {
            'authenticity_token': self.csrf,
            'user_id': self.users_id[0],
            'transfer_opportunities': 'false',
            'transfer_opportunities': 'false',
            'nowin_opportunities': 'false',
            'opportunity_ids[]': opportunities_id[0],
            'opportunity_ids[]': opportunities_id[1],
            'opportunity_ids[]': opportunities_id[2]
        }
        response = self.common.put_response_json(url, body, '批量转移商机')
        # if not response:
        #     return {}
        # self.response = response
        # return self.response.json()
        return response

    # 获取所有的用户id
    def users_get_all(self):
        url = self.base_url + 'api/users'
        params = {
            'username': '',
            'page': 1,
            'perPage': 15
        }
        response = self.common.get_response_json(url, params, '获取用户')
        if not response:
            return {}
        user_models = response.json()['models']
        user_ids = []
        for user in user_models:
            user_ids.append(user['id'])
        return user_ids

    # 获取商机的id list
    def get_opportunity_ids(self, scope):
        url = self.base_url + 'opportunities'
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': 'opportunities.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取所有的商机')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        checked_opportunitie = soup.find(attrs={'data-entity-table-name': 'opportunitie'})
        if checked_opportunitie:
            a = str(checked_opportunitie)
            opportunity_ids = re.findall(r"data-id=\"(.*?)\">", a)
            return opportunity_ids

    # 批量添加协作人
    def opportunities_add_assist_user(self, scope, opportunity_ids):
        url = self.base_url + 'batch_edit_assist_user/field_form'
        params = {
            'model': 'opportunitie'
        }
        response = self.common.get_response_json(url, params, '打开添加协作人的窗口')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, 'html.parser')
        assit_user_content = soup.find(attrs={'id': 'opportunitie_assist_user_ids'})
        # 获取所有下拉框中的用户对应的id
        assit_users = re.findall(r"value=(.*?)>", str(assit_user_content))
        url = self.base_url + 'api/opportunities/batch_update_assist_user'
        for operation_selection in const.opportunitie_ADD_ASSIST_USER_OPERATION_SELECTION:
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'operation_selection': operation_selection,
                'opportunitie[assist_user_ids][]': '',
                'opportunitie[assist_user_ids][]': assit_users[0],
                'opportunitie[assist_user_ids][]': assit_users[1],
                'ids[]': opportunity_ids[0],
                'ids[]': opportunity_ids[1]
            }
            response = self.common.put_response_json(url, body, '给所选的商机添加协作人:' + '添加的操作是 is:' + operation_selection)
            if not response:
                return {}
            # if not response:
            #     return {}
            # self.response = response
            # return self.response.json()

    # 给商机添加协作人
    def add_assist_user_for_opportunitie(self, opportunity_id):
        url = self.base_url + 'opportunities/' + str(opportunity_id) + '/edit_assist_user'
        params = {}
        response = self.common.get_response_json(url, params, '商机详情页打开添加协作人的窗口')

        url = self.base_url + 'api/opportunities/' + str(opportunity_id) + '/update_assist_user'
        self.users_id = self.users_get_all()
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'opportunitie[id]': opportunity_id,
            'opportunitie[assist_user_ids][]': '',
            'opportunitie[assist_user_ids][]': self.users_id[0],
            'opportunitie[assist_user_ids][]': self.users_id[1]
        }
        self.common.post_response_json(url, body, '商机详情页给该商机添加协作人')

    # 给当前商机添加附件
    def upload_attachment_for_current_opportunity(self, opportunity_id):
        url = self.base_url + 'attachments/' + str(opportunity_id) + '/add_attachment'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'klass': 'opportunitie',
            'attachment_ids[]': 123456,
            'note': ''
        }
        self.common.post_response_json(url, body, '商机详情页添加附件')

    # 新建任务
    def create_event_for_opportunitie(self, opportunity_id):
        url = self.base_url + 'events/new'
        params = {
            'ajax_back_to': '/events?entity_id=' + str(opportunity_id) + '&entity_klass=opportunitie',
            'entity_id': opportunity_id,
            'entity_klass': 'opportunitie'
        }
        response = self.common.get_response_json(url, params, '打开新建任务窗口')
        url = self.base_url + 'api/events'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'event[note]': '给客户打电话',
            'event[remind_at]': '2018-03-02 17:19',
            'event[remind_type]': 'punctual',
            'event[related_item_id]': opportunity_id,
            'event[related_item_type]': 'opportunitie',
            'event[user_ids]': self.users_get_all()[0]
        }
        response = self.common.post_response_json(url, body, '商机详情页创建任务')
        if not response:
            return {}
        self.response = response
        event_id = response.json()['data']['id']
        return event_id

    #
    # # #新建任务
    # def create_event_for_opportunitie(self, opportunity_id):
    #     url = self.base_url + 'api/events'
    #     body = {
    #         'utf8': '✓',
    #         'authenticity_token': self.csrf,
    #         'event[note]': '给客户打电话',
    #         'event[remind_at]': '2018-06-28 17:19',
    #         'event[remind_type]': 'punctual',
    #         'event[related_item_id]': opportunity_id,
    #         'event[related_item_type]': 'opportunitie',
    #         'event[user_ids]': self.users_get_all()[0]
    #     }
    #     # response = self.common.post_response_json(url, body, '商机详情页创建任务')
    #     response = self.common.post_json_response_json(url, body, '商机详情页创建任务')
    #     if not response:
    #         return {}
    #     self.response = response
    #     event_id = response.json()['data']['id']
    #     return event_id

    # 将任务设为已完成
    def update_event_complete(self, event_id):
        url = self.base_url + 'api/reminders/' + str(event_id) + '/update_status'
        params = {
            'remind_status': 'complete'
        }
        self.common.get_response_json(url, params, '把任务设置成已完成')

    # 将任务设为未完成
    def update_event_todo(self, event_id):
        url = self.base_url + 'api/reminders/' + str(event_id) + '/update_status'
        params = {
            'remind_status': 'todo'
        }
        self.common.get_response_json(url, params, '设置任务为未完成')

    # 获取当前用户为完成的任务
    def get_event_todo(self, opportunity_id):
        url = self.base_url + 'api/events/count_by_status'
        params = {
            'entity_id': opportunity_id,
            'entity_klass': 'opportunitie',
            'status': 'expired_and_todo'
        }
        self.common.get_response_json(url, params, '获取所有已完成的任务')


    # # 审批商机
    # def approve_opportunitie(self, opportunity_id):
    #     url = self.base_url + 'api/approvals/' + str(opportunity_id) + '/approve'
    #     body = {
    #         'utf8': '✓',
    #         '_method': 'put',
    #         'authenticity_token': self.csrf,
    #         'key': 'opportunitie',
    #         'opportunitie[step]': '1',
    #         'opportunitie[approve_description]': '审批通过',
    #         'opportunitie[notify_user_ids][]': '',
    #     }
    #     self.common.post_response_json(url, body, '审批商机通过')
    #
    # # 审批否决商机
    # def deny_opportunitie_approve(self, opportunity_id):
    #     url = self.base_url + 'api/approvals/' + str(opportunity_id) + '/deny'
    #     body = {
    #         'utf8': '✓',
    #         '_method': 'put',
    #         'authenticity_token': self.csrf,
    #         'key': 'opportunity',
    #         'opportunity[approve_description]': '不予通过',
    #         'opportunity[step]': '1'
    #     }
    #     self.common.post_response_json(url, body, '审批否决商机')
    #
    #
    # # 审批时编辑通知他人
    # def update_notify_user(self, opportunity_id, user_id):
    #     url = self.base_url + 'api/approvals/' + str(opportunity_id) + '/update_notify_users'
    #     body = {
    #         'utf8': '✓',
    #         '_method': 'put',
    #         'authenticity_token': self.csrf,
    #         'key': 'opportunitie',
    #         'opportunity[notify_user_ids][]': user_id,
    #     }
    #     self.common.post_response_json(url, body, '审批通过时通知他人')