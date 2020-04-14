from bs4 import  BeautifulSoup
import re
import random
import string
from commons  import  common
from commons.const import const
from testCase.leads.testGetLeads import GetLeads


class revisit_logs:
    def __init__(self, cookie, csrf):
        self.common = common.Common(cookie, csrf)
        self.base_url = const.BASE_URL
        self.base_url2 = const.SIGN_IN_BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.get_lead_ids = GetLeads(cookie, csrf)
        pass

    # 获取各模块跟进状态和跟进类型
    def get_visit_way_list(self):
        url = self.base_url + 'field_maps'
        body = {}
        response = self.common.get_response_json(url , body , 'get_page')
        soup = BeautifulSoup(response.content,'html.parser')
        lead_way= str(str(soup).split('跟进状态')[1]).split('渠道')[0]
        lead_status = re.findall(r' data-fieldvalue-id=\"(\d+)\"',str(lead_way))
        customer_way =  str(str(soup).split('跟进状态')[2]).split('客户类型')[0]
        customer_status = re.findall(r' data-fieldvalue-id=\"(\d+)\"',str(customer_way))
        opportunity_way =  str(str(soup).split('销售阶段')[1]).split('商机类型')[0]
        opportunity_status = re.findall(r' data-fieldvalue-id=\"(\d+)\"',str(opportunity_way))
        contract_way =  str(str(soup).split('合同状态')[1]).split('回款类型')[0]
        contract_status = re.findall(r' data-fieldvalue-id=\"(\d+)\"',str(contract_way))
        visit_way =  str(str(soup).split('跟进类型')[1]).split('费用类型')[0]
        visit_way_list = re.findall(r' data-fieldvalue-id=\"(\d+)\"',str(visit_way))
        return lead_status,customer_status,opportunity_status,contract_status,visit_way_list

    def add_lead_revisit_log(self):
        lead_list = self.get_lead_ids.lead_ids()
        url = self.base_url +'api/leads/' + str(lead_list[0]) + '/revisit_logs?lead_id=' + str(lead_list[0])
        body = {
            'utf8': '✓',
            'authenticity_token': self.csrf,
            'request_ticket':  ''.join(random.sample(string.ascii_letters + string.digits, 12)),
            'revisit_log[category]': self.get_visit_way_list()[4][0],
            'revisit_log[real_revisit_at]': '2019-02-27 14:32:11',
            'revisit_log[content]': '存在存vxcvxcbvcb在需自行车'''.join(random.sample(string.ascii_letters + string.digits, 10)),
            'revisit_log[loggable_attributes][status]': self.get_visit_way_list()[0][0],
            'revisit_log[loggable_attributes][id]': lead_list[0],
            'revisit_log[remind_at]':''
        }
        response = self.common.post_response_json(url , body,"add_lead_revisit_log")
        print(response.json())




