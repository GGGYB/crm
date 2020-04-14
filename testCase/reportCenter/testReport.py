# -*- coding: utf-8 -*-
__author__ = 'Sally Wang'

from commons import common
from commons.const import const
from .testRevisitLogs import RevisitLogs
from .testOpportunitiesReport import Opportunities
from .testSalesFunnelReport import SalesFunnel
from .testEntitiesAddReport import EntitiesAdd
from .testReportCenter import ReportCenter
from .testGoalStats import GoalStats
from .testWonStats import WonStats
from .testContactStats import ContractsStats
from .testVisitInfo import VisitInfo
from .testLeadTransRate import LeadTransRate
from .testWonRank import WonRank
from .testCustomerCategories import CustomerCategoried
from .testSocialShareStats import SocialShareStats
from .testSMSReachRateStats import SMSReachRateStats
from .testReceivedPayments import ReceivedPayments
from .testCustomersRank import CustomerRank
from .testGoalStats import GoalStats
from .testProductSaesStats import ProductSalesStats
from .testGoalRank import GoalRank

class Report:
    def __init__(self, cookie, csrf):
        self.base_url = const.BASE_URL
        self.csrf = csrf
        self.cookie = cookie
        self.common = common.Common(cookie, csrf)
        self.revisit_log = RevisitLogs(cookie, csrf)
        self.opportunities_report = Opportunities(cookie, csrf)
        self.sales_funnel_report = SalesFunnel(cookie, csrf)
        self.entities_add_report = EntitiesAdd(cookie, csrf)
        self.report_center = ReportCenter(cookie, csrf)
        self.won_stats = WonStats(cookie, csrf)
        self.contract_stats = ContractsStats(cookie, csrf)
        self.visit_info = VisitInfo(cookie, csrf)
        self.lead_trans_rate = LeadTransRate(cookie, csrf)
        self.won_rank = WonRank(cookie, csrf)
        self.customer_categories = CustomerCategoried(cookie, csrf)
        self.social_shre_stats = SocialShareStats(cookie, csrf)
        self.sms_reach_rate_stats = SMSReachRateStats(cookie, csrf)
        self.received_payments = ReceivedPayments(cookie, csrf)
        self.customer_rank = CustomerRank(cookie, csrf)
        self.goal_stats = GoalStats(cookie, csrf)
        self.product_sales_stats = ProductSalesStats(cookie, csrf)
        self.goal_rank = GoalRank(cookie, csrf)
        pass

    def testReport(self):
        #销售过程类
        #跟进记录报表
        self.revisit_log.testRevistLogReportByDimension()
        # #销售预测报表
        self.opportunities_report.testOpportunities()
        # #销售漏斗报表
        self.sales_funnel_report.testSalesFunnel()
        # #业务新增汇总报表
        self.entities_add_report.testEntitiesAddByDimension()
        ###销售业绩类
        ##业绩目标完成度报表
        self.goal_stats.testGoalStats()
        # #回款计划汇总报表
        self.report_center.testReportCenter()
        ###销售业绩类/产品销售汇总报表
        self.product_sales_stats.testProductSalesStatsByDimension()
        # #赢单商机汇总报表
        self.won_stats.testWonStats()
        # #合同汇总报表
        self.contract_stats.testContractsStats()
        # #销售管理类/拜访签到表
        self.visit_info.testVisitInfo()
        # #销售管理类/销售回款排名报表
        self.received_payments.testReceivedPayments()
        # #销售管理类/客户数量排名报表
        self.customer_rank.testCustomerRank()
        #销售管理类/业绩目标完成度排名报表
        self.goal_rank.testGoalRank()
        # #销售管理类/销售额排名报表
        self.won_rank.testWonRank()
        # #销售管理类/线索转化率
        self.lead_trans_rate.testLeadTransRate()
        # # 销售额排名报表
        # #分析类/客户类型统计报表
        self.customer_categories.testCustomerCategoried()
        # #分析类/短信转化率报表
        self.social_shre_stats.testSocialShareStats()
        # 分析类/短信到达率报表
        self.sms_reach_rate_stats.testSMSReachRateStats()