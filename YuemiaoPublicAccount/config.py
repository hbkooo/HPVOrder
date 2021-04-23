# encoding: utf-8
"""
配置文件信息，用户需要在这里配置自己的个人信息
"""

# 获取全国各地的城市、区的编号，将其保存文件路径
save_city_code_root = 'data/city_info'

# 保存某一个社区医院的信息
save_departments_info_root = 'data/departments'

# 疫苗类型，3-九价疫苗；2-四价疫苗；1-二价疫苗进口；52-二价疫苗国产。默认是九价
customId = 3

# 需要打第几针
vaccIndex = 1

# 抢苗的用户姓名，需要已经在系统中注册该用户名
username = '张三'

# 疫苗规格信息，用户无需修改
VACCINDE_INFO = {
    3: '九价疫苗',
    2: '四价疫苗',
    1: '二价（进口）疫苗',
    52: '二价（国产）疫苗',
}

# [error] :  URL:https://wx.scmttec.com/passport/register/isNeedRegister.do ERROR:500 Server Error: Internal Server Error for url: https://wx.scmttec.com/passport/register/isNeedRegister.do?depaCode=4109020008&departmentVaccineId=7694&vaccineCode=8803&linkmanId=8350927

URLS = {
    # 地区信息, GET
    "INFO": "https://wx.scmttec.com/base/region/childRegions.do",
    # 根据区域id获取该区域所有的医院，POST
    "ALL_DEPARTMENTS": "https://wx.scmttec.com/base/department/getDepartments.do",
    # 获取某个医院的具体信息，GET
    "DEPARTMENT": "https://wx.scmttec.com/base/departmentVaccine/item.do",
    # 疫苗信息
    "VACCINE_INFO": "https://wx.scmttec.com/base/department/vaccine.do",
    # 查看当前所有的用户信息
    "ALL_USER": "https://wx.scmttec.com/order/linkman/findByUserId.do",
    # 当前时间
    "TIME_NOW": "https://wx.scmttec.com/base//time/now.do",
    # 在某个医院界面中点击立即预约
    "JUDGE_ORDER": "https://wx.scmttec.com/order/subscribe/isCanSubscribe.do",
    "JUDGE_REGISTER": "https://wx.scmttec.com/passport/register/isNeedRegister.do",
    "CHOOSE_NUM": "https://wx.scmttec.com/order/subscribe/workDays.do",                         # 获取该针可预约的日期
    "GET_MAX_ORDER": "https://wx.scmttec.com/order/subscribe/findSubscribeAmountByDays.do",     # 获取请求日期的可预约人数
    "CHOOSE_TIME_OF_DAY": "https://wx.scmttec.com/order/subscribe/departmentWorkTimes2.do",     # 选择某一天后得到该天的可预约时间段
    "START_ORDER": "https://wx.scmttec.com/order/subscribe/add.do",
    # 预约成功后可以看到预约的消息
    "ORDER_INFO": "https://wx.scmttec.com/order/subscribe/clientDetail.do",
    # 在某个部门订阅
    "SUBSCRIBE_CHECK": "https://wx.scmttec.com/passport/register/checkLinkman.do",
    "SUBSCRIBE": "https://wx.scmttec.com/passport/register/subscibe.do",
    # 查看某个订阅的详细信息
    "SUBSCRIBE_INFO": "https://wx.scmttec.com/passport/register/myRegisterItem.do",
    "SUBSCRIBE_INFO_RANK": "https://wx.scmttec.com/passport/register/registerRanking.do",
    # 取消订阅
    "DELETE_SUBSCRIBE": "https://wx.scmttec.com/passport/register/delete.do",
    # 用户的所有的订阅信息
    "ALL_SUBSCRIBE": "https://wx.scmttec.com/passport/register/myRegisterList.do",
    # 查找用户
    "USER": "https://wx.scmttec.com/order/linkman/findByUserId.do",

    # 获取代理IP
    "IP_PROXY": "https://ip.jiangxianli.com/api/proxy_ips",
    # 服务器当前时间戳
    "SERVER_TIME": "https://miaomiao.scmttec.com/seckill/seckill/now2.do",
    # 疫苗列表
    "VACCINE_LIST": "https://miaomiao.scmttec.com/seckill/seckill/list.do",
    # 校验库存
    "CHECK_STOCK": "https://miaomiao.scmttec.com/seckill/seckill/checkstock2.do",
    # 接种人信息
    "USER_INFO": "https://miaomiao.scmttec.com/seckill/linkman/findByUserId.do",
    # 秒杀疫苗
    "SEC_KILL": "https://miaomiao.scmttec.com/seckill/seckill/subscribe.do"
}

# common headers
REQ_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; COR-AL10 Build/HUAWEICOR-AL10; wv) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045511 Mobile Safari/537.36 "
                  "MMWEBID/9684 MicroMessenger/7.0.18.1740(0x2700123B) Process/tools WeChat/arm64 NetType/WIFI "
                  "Language/zh_CN ABI/arm64",
    "Referer": "https://wx.scmttec.com/index.html",
    "Accept": "application/json, text/plain, */*",
    "Host": "wx.scmttec.com"
}

