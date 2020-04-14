# coding:utf-8
import os
import sys
import time
import unittest
from co import HTMLTestRunner
from co import send

# reload(sys)
# sys.setdefaultencoding('utf8')


def all_case():
    # 待执行用例的目录
    case_dir = os.path.join(os.getcwd(), "case")

    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir,pattern="Testapi.py",top_level_dir=None)
    # 所有test开头的文件
    # discover = unittest.defaultTestLoader.discover(case_dir,
    #                                                pattern="test*.py",
    #                                                top_level_dir=None)
    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
        # 添加用例到 testcase
            testcase.addTests(test_case)
            print (testcase)
            return testcase
if __name__ == "__main__":
    # 返回实例
    runner = unittest.TextTestRunner()
    nowtime = time.strftime("%m_%d_%H_%M_%S")
    report_path = os.path.join(os.getcwd(), "report", nowtime + ".html")
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'这是ding-staging接口自动化测试报告',
                                           description=u'用例执行情况：')

    runner.run(all_case())
    fp.close()


    send.send_main(report_path, nowtime + ".html")
