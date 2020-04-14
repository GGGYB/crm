#coding:utf-8

class const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

const = const()

# test环境调试
const.BASE_URL = 'https://ik-test.ikcrm.com/'
const.SIGN_IN_BASE_URL = 'https://uc-test.weiwenjia.com/api/sso/'
# test钉钉环境调试
# const.BASE_URL = 'https://ding-test.ikcrm.com/'
# const.SIGN_IN_BASE_URL = 'https://ding-test.ikcrm.com/api/v2/auth/login'
# apptoken ="f6620ff6729345c8b6101174e695d0ab"
# staging钉钉环境调试
# const.BASE_URL = 'https://ding-staging.ikcrm.com/'
# const.SIGN_IN_BASE_URL = 'https://ding-staging.ikcrm.com/api/v2/auth/login'
#Staging环境域名
# const.BASE_URL = 'https://ik-staging.ikcrm.com/'
# const.SIGN_IN_BASE_URL = 'https://uc-staging.weiwenjia.com/api/sso/'
#生产环境域名
# const.BASE_URL = 'https://e.ikcrm.com/'
# const.SIGN_IN_BASE_URL = 'https://www.ikcrm.com/users/sign_in/'

const.REPORT_TIME = ['all', 'today','week','month','quarter','year','other']
const.SCOPE = ['all_own', 'my_own', 'my_assist']
const.DUPLICATE = ['customer', 'lead', 'contact']
# 独立版本
# const.USER = [{'username': '15639354511', 'password': '111111','role':'开通搜客宝和电销超管'}, {'username': '14526378956', 'password': '111111','role':'开通搜客宝和电销非超管'},
#               {'username': '19512340001', 'password': '111111','role':'开通电销超管'},{'username': '19512340002', 'password': '111111','role':'开通电销非超管'},
#               {'username': '15601716120', 'password': '111111','role':' 开通搜客宝超管'},{'username': '18749947152', 'password': '111111','role':' 开通搜客宝非超管'},
#               {'username': '19512345678', 'password': '111111','role':'没有开通电销版和搜客宝的超管'},{'username': '19212345678', 'password': '111111','role':'没有开通电销版和搜客宝非超管'},
#               {'username': '15652325652', 'password': '111111','role':'没有开通电销版和搜客宝的超管'}]
# const.USER = [
#             {'username': '15000249334', 'password': 'Ik123456', 'role': '1','usertitle':'设计部-用户1','departments':['设计部']},
#              {'username': '15000278040', 'password': 'Ik123456', 'role': '2','usertitle':'设计部-用户2','departments':['设计部']},
#             {'username': '18049905933', 'password': 'Ik123456', 'role': '3','usertitle':'产品部-用户3','departments':['产品部']},
#             {'username': '18049903011', 'password': 'Ik123456', 'role': '4','usertitle':'设计部子部门-用户4','departments':['设计部子部门']},
#             {'username': '13622222222', 'password': 'Ik123456', 'role': '5','usertitle':'销售部-用户5','departments':['销售部']},
#             {'username': '13799999999', 'password': 'Ik123456', 'role': '6','usertitle':'主辅部门-用户6','departments':['设计部','产品部']}
#             ,{'username': '15033333333', 'password': 'Ik123456', 'role': '7','usertitle':'同部门下属-用户7','departments':['设计部']},
#             {'username': '15044444444', 'password': 'Ik123456', 'role': '8','usertitle':'设计部二级部门-用户8','departments':['设计部二级部门']}
#         ]
# const.USER = [{'username': '15000249334 ', 'password': 'Ik123456','role':'没有开通电销版和搜客宝的超管'}]
const.USER = [{'username': '18721277192 ', 'password': 'Ik123456','role':'没有开通电销版和搜客宝的超管'}]
# const.USER = [{'uid': '4009563','role':'没有开通电销版和搜客宝的超管'},{'uid': '4009569','role':'没有开通电销版和搜客宝的普通用户'}]
const.CUSTOMER_ADD_ASSIST_USER_OPERATION_SELECTION = ['append_assist_user', 'replace_assist_user', 'remove_assist_user']

# 1. 开通电销版的超管
# 13600000003     111111
# 2. 开通电销版的非超管
# 13699990000  111111
# 3. 开通搜客宝的超管
# 15317839529  111111
# 4. 开通搜客宝的非超管用户
# 19112340006  111111
# 5. 没有开通电销版和搜客宝的超管
# 17092939095   1111111
# 6. 没有开通电销版和搜客宝的非超管
# 17719601895  111111