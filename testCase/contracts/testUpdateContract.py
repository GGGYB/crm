# -*- coding: utf-8 -*-
__author__ = 'Jun'

from bs4 import BeautifulSoup
import json
import requests
import random
import datetime
import re
from decimal import Decimal as D
from commons import common
from commons.const import const
from .testAddContract import AddContract


class UpdateContract:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.response = ''
        self.users_id = []
        self.contracts_id = []



    def update_contracts_by_scope(self, scope, contracts_id):
        self.quick_edit_contracts(scope, contracts_id)
        self.contracts_field_update(scope, contracts_id)
        # 批量转移合同
        self.contracts_mass_transfer(scope, contracts_id)
        # 批量添加协作人
        self.contracts_add_assist_user(scope, contracts_id)

        for contract_id in contracts_id:
            self.add_assist_user_for_contract(contract_id)
            self.upload_attachment_for_current_contract(contract_id)
            event_id = self.create_event_for_contract(contract_id)
            self.update_event_complete(event_id)
            self.update_event_todo(event_id)
            self.get_event_todo(contract_id)

    # 批量编辑
    def contracts_field_update(self, scope, contract_ids):
        url = self.base_url + 'batch_edit/field_form?model=Contract'
        params = {
            'model': 'Contract'
        }
        response = self.common.get_response_json(url, params, '打开编辑合同的窗口')
        if response != False:
            S = response.content
            soup = BeautifulSoup(S, 'html.parser')
            optional_field = soup.find(attrs={'id': 'field_choice'})
            fields = re.findall(r"value=\"(.*?)\">", str(optional_field))
            selected_fields = soup.findAll(attrs={'class': 'batch-edit-custom-field hidden'})
            selected_field_list = []
            for i in selected_fields:
                selected_field = re.findall(r"value=\"(.*?)\">", str(i))
                selected_field_list.append(selected_field)
            url = self.base_url + 'api/contracts/batch_update'
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'field_choice': fields[3],
                'contract[' + fields[3] + ']': selected_field_list[2][2],
                'ids[]': contract_ids[0],
                'ids[]': contract_ids[1]
            }
            response = self.common.put_response_json(url, body, '批量编辑合同')
            return response

    # 快捷编辑合同
    def quick_edit_contracts(self, scope, contract_id):
        url = self.base_url + 'quick_edit/field_form?model=Contract&id='+str(contract_id)+ '&field_name=total_amount&page_type=index&_=1534589066751'
        params = {
            'model': 'contract',
            'id': contract_id,
            'field_name': 'name',
            'page_type': 'index'
        }
        self.common.get_response_json(url, params, '快捷编辑合同获取当前合同的field name')
        url = self.base_url + 'api/contracts/' + str(contract_id)
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.csrf,
            'contract[id]': contract_id,
            'common_id': '',
            'contract[total_amount]': '50000'
        }
        response = self.common.put_response_json(url, body, '快捷编辑合同，编辑的字段是：')
        if not response:
            return {}
        self.response = response
        return self.response.json()

    # 快捷编辑单个合同
    # def quick_edit_contract(self, new_value, contract_id):
    #     url = self.base_url + 'quick_edit/field_form'
    #     params = {
    #         'model': 'contract',
    #         'id': contract_id,
    #         'field_name': 'name',
    #         'page_type': 'index'
    #     }
    #     self.common.get_response_json(url, params, '快捷编辑合同获取当前合同的field name')
    #
    #     url = self.base_url + 'api/contracts/' + str(contract_id)
    #     body = {
    #         'utf8': '✓',
    #         '_method': 'patch',
    #         'authenticity_token': self.csrf,
    #         'contract[id]': contract_id,
    #         'common_id': '',
    #         'contract[name]': new_value
    #     }
    #     response = self.common.put_response_json(url, body, '快捷编辑合同，编辑的字段是：')
    #     if not response:
    #         return {}
    #     self.response = response
    #     return self.response.json()
    # 批量转移合同
    def contracts_mass_transfer(self, scope, contracts_id):
        url = self.base_url + 'api/contracts/mass_transfer'
        self.users_id = self.users_get_all()
        body = {
            'authenticity_token': self.csrf,
            'user_id': self.users_id[0],
            'transfer_contracts': 'false',
            'transfer_opportunities': 'false',
            'nowin_opportunities': 'false',
            'contract_ids[]': contracts_id[0],
            'contract_ids[]': contracts_id[1],
            'contract_ids[]': contracts_id[2]
        }
        response = self.common.put_response_json(url, body, '批量转移合同')
        return response

    # 获取所有的用户id
    def users_get_all(self):
        url = self.base_url + 'api/users'
        params = {
            'username': '',
            'page': 1,
            'perPage': 15
        }
        response = self.common.get_response_json(url, params, '获取用户************')
        if not response:
            return {}
        user_models = response.json()['models']
        user_ids = []
        for user in user_models:
            user_ids.append(user['id'])
        return user_ids

    # 获取合同的id list
    def get_contract_ids(self, scope):
        url = self.base_url + 'contracts'
        params = {
            'order': 'asc',
            'scope': scope,
            'sort': 'contracts.updated_at desc',
            'per_page': '10',
            'type': 'advance',
            'section_only': 'true'
        }
        response = self.common.get_response_json(url, params, '获取所有的合同************')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        checked_contract = soup.find(attrs={'data-entity-table-name': 'contract'})
        if checked_contract:
            a = str(checked_contract)
            contract_ids = re.findall(r"data-id=\"(.*?)\">", a)
            return contract_ids

    # 批量添加协作人
    def contracts_add_assist_user(self, scope, contract_ids):
        url = self.base_url + 'batch_edit_assist_user/field_form'
        params = {
            'model': 'contract'
        }
        response = self.common.get_response_json(url, params, '打开添加协作人的窗口')
        if not response:
            return {}
        self.response = response
        S = self.response.content
        soup = BeautifulSoup(S, 'html.parser')
        assit_user_content = soup.find(attrs={'id': 'contract_assist_user_ids'})
        # 获取所有下拉框中的用户对应的id
        assit_users = re.findall(r"value=(.*?)>", str(assit_user_content))
        url = self.base_url + 'api/contracts/batch_update_assist_user'
        for operation_selection in const.contract_ADD_ASSIST_USER_OPERATION_SELECTION:
            body = {
                'utf8': '✓',
                'authenticity_token': self.csrf,
                'operation_selection': operation_selection,
                'contract[assist_user_ids][]': '',
                'contract[assist_user_ids][]': assit_users[0],
                'contract[assist_user_ids][]': assit_users[1],
                'ids[]': contract_ids[0],
                'ids[]': contract_ids[1]
            }
            response = self.common.put_response_json(url, body, '给所选的合同添加协作人:' + '添加的操作是 is:' + operation_selection)
            if not response:
                return {}
            # if not response:
            #     return {}
            # self.response = response
            # return self.response.json()

    # 给合同添加协作人
    def add_assist_user_for_contract(self, contract_id):
        url = self.base_url + 'contracts/' + str(contract_id) + '/edit_assist_user'
        params = {}
        response = self.common.get_response_json(url, params, '合同详情页打开添加协作人的窗口')

        url = self.base_url + 'api/contracts/' + str(contract_id) + '/update_assist_user'
        self.users_id = self.users_get_all()
        body = {
            'utf8': '✓',
            '_method': 'patch',
            'contract[id]': contract_id,
            'contract[assist_user_ids][]': '',
            'contract[assist_user_ids][]': self.users_id[0],
            'contract[assist_user_ids][]': self.users_id[1]
        }
        self.common.post_response_json(url, body, '合同详情页给该合同添加协作人')

    # 给当前合同添加附件
    def upload_attachment_for_current_contract(self, contract_id):
        url = self.base_url + 'attachments/' + str(contract_id) + '/new_attachment?klass=Contract'
        'https://ik-staging.ikcrm.com/api/qiniu/auth/upload_token.json?policy=attachment'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'klass': 'Contract',
            'attachment_ids[]': 123456,
            'note': ''
        }
        self.common.post_response_json(url, body, '合同详情页添加附件')

    # 新建任务
    def create_event_for_contract(self, contract_id):
        url = self.base_url + 'events/new?ajax_back_to=%2Fevents%3Fentity_id%3D30915%26entity_klass%3DContract&entity_id='+str(contract_id)+'&entity_klass=Contract'
        params = {
            'ajax_back_to': '/events?entity_id='+str(contract_id)+'&entity_klass=Contract',
            'entity_id': contract_id,
            'entity_klass': 'Contract'
        }
        response = self.common.get_response_json(url, params, '打开新建任务窗口')
        url = self.base_url + 'api/events'
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'event[note]': '给客户打电话',
            'event[remind_at]': '2018-03-02 17:19',
            'event[remind_type]': 'punctual',
            'event[related_item_id]': contract_id,
            'event[related_item_type]': 'contract',
            'event[user_ids]': self.users_get_all()[0]
        }
        response = self.common.post_response_json(url, body, '合同详情页创建任务')
        if not response:
            return {}
        self.response = response
        event_id = response.json()['data']['id']
        return event_id


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
    def get_event_todo(self, contract_id):
        url = self.base_url + 'api/events/count_by_status'
        params = {
            'entity_id': contract_id,
            'entity_klass': 'contract',
            'status': 'expired_and_todo'
        }
        self.common.get_response_json(url, params, '获取所有已完成的任务')

    # 审批合同
    def approve_contract(self, contract_id):
        url = self.base_url + 'api/approvals/' + str(contract_id) + '/approve'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'contract',
            'contract[step]': '1',
            'contract[approve_description]': '审批通过',
            'contract[notify_user_ids][]': '',
        }
        self.common.post_response_json(url, body, '审批合同通过')

    # 审批否决合同
    def deny_contract(self, contract_id):
        url = self.base_url + 'api/approvals/' + str(contract_id) + '/deny'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'contract',
            'contract[approve_description]': '不予通过',
            'contract[step]': '1'
        }
        self.common.post_response_json(url, body, '审批否决合同')

    # 审批时编辑通知他人
    def update_notify_user(self, contract_id, user_id):
        url = self.base_url + 'api/approvals/' + str(contract_id) + '/update_notify_users'
        body = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': self.csrf,
            'key': 'contract',
            'contract[notify_user_ids][]': user_id,
        }
        self.common.post_response_json(url, body, '审批通过时通知他人')