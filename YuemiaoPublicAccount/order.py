# encoding: utf-8
"""
预定疫苗的各种操作
"""
import hashlib
import os.path as osp
import time as sysTime
from YuemiaoPublicAccount.util import save_json, GET, get_server_time, get_server_time_miaomiao
from YuemiaoPublicAccount.linkman import get_linkmanId_by_name
from YuemiaoPublicAccount.department_info import get_department_vaccine_info
from YuemiaoPublicAccount.vaccine import get_vaccine_info
import YuemiaoPublicAccount.config as cfg
from thirdparty.send_text_message import send_text_message


# 打印抢到的疫苗的详细信息
def print_my_order_success_info(data):
    """
    打印输出预约成功的信息
    :param data: 查询到的预约成功的详细信息
    "data":{
                "department":{
                    "address":"郑东新区康平路与榆林北路交叉口西北角",
                    "code":"4101040014",
                    "isPay":0,
                    "isSupplier":0,
                    "latitude":34.757124,
                    "longitude":113.761923,
                    "name":"郑州唯爱康中医院",
                    "serviceFee":0,
                    "tel":"0371-86561607",
                    "worktimeDesc":"周一至周六上午8点至11点半，下午2点至4点，周日上午8点至11点半，单针预约。\n儿童接种请带接种本，成人接种请带身份证。"
                },
                "departmentWorktime":{
                    "endTime":"11:30",
                    "startTime":"08:00"
                },
                "endTime":1610467852000,
                "isUpdate":true,
                "nowTime":1610466055048,
                "subscribe":{
                    "birthday":"1996-08-02 00:00:00",
                    "cancelWay":1,
                    "createTime":"2021-01-12 23:40:52",
                    "depaCode":"4101040014",
                    "departmentVaccineId":12302,
                    "id":4295641,
                    "inoclateVerifyCode":"101509",
                    "isPay":0,
                    "isSeckill":false,
                    "isSubscribeAll":0,
                    "linkmanId":8350927,
                    "mobile":"15927037762",
                    "onlinePaymentPrice":0,
                    "serviceFee":0,
                    "status":0,
                    "subscribeDate":"2021-01-14 00:00:00",
                    "userId":9787092,
                    "userNickName":"刘香玉",
                    "vaccinePrice":35100
                },
                "subsequentEstimatedTime":[
                    {
                        "estimatedDate":"2021-02-14",
                        "vaccineIndex":"2"
                    },
                    {
                        "estimatedDate":"2021-07-14",
                        "vaccineIndex":"3"
                    }
                ],
                "vaccine":{
                    "ageEnd":45,
                    "ageStart":9,
                    "code":"8806",
                    "factoryName":"厦门万泰沧海生物技术有限公司",
                    "inoculateIndex":1,
                    "name":"二价HPV疫苗（国产）",
                    "price":35100,
                    "specifications":"0.5ml/瓶"
                }
            },
    :return: None
    """
    # 社区信息
    department = data['department']
    address = department['address']
    departmentName = department['name']
    tel = department['tel']
    worktime_start = data['departmentWorktime']['startTime']
    worktime_end = data['departmentWorktime']['endTime']

    # 个人用户信息
    subscribe = data['subscribe']
    username = subscribe['userNickName']
    mobile = subscribe['mobile']
    subscribeDate = subscribe['subscribeDate']

    # 疫苗信息
    vaccine = data['vaccine']
    current_vaccine_index = vaccine['inoculateIndex']
    factoryName = vaccine['factoryName']
    vaccine_name = vaccine['name']

    # 剩余针的信息
    next_vaccine = data['subsequentEstimatedTime']

    print()
    print('#' * 50)
    print('#' * 20 + '抢到的疫苗的信息' + '#' * 20)
    print('#' * 50)
    print('用户信息：')
    print('用户姓名：', username)
    print('用户手机：', mobile)
    print('用户注射时间：', subscribeDate)

    print('社区信息：')
    print('社区名称：', departmentName)
    print('社区地址：', address)
    print('社区电话：', tel)
    print('社区工作时间：{} - {}'.format(worktime_start, worktime_end))

    print('疫苗信息：')
    print('疫苗名称：', vaccine_name)
    print('疫苗针次：', vaccine_name)
    print('疫苗厂商：', factoryName)
    for next in next_vaccine:
        print('剩余的第 {} 针疫苗注射时间 {}'.format(next['vaccineIndex'], next['estimatedDate']))


# 查询详细的预约信息
def get_my_order_info_by_subscribeId(subscribeId):
    """
    查询详细的预约信息
    :param subscribeId: 预约成功后会返回的这个预约 id 号
    :return:
        {
            "code":"0000",
            "data":{
                "department":{
                    "address":"郑东新区康平路与榆林北路交叉口西北角",
                    "code":"4101040014",
                    "isPay":0,
                    "isSupplier":0,
                    "latitude":34.757124,
                    "longitude":113.761923,
                    "name":"郑州唯爱康中医院",
                    "serviceFee":0,
                    "tel":"0371-86561607",
                    "worktimeDesc":"周一至周六上午8点至11点半，下午2点至4点，周日上午8点至11点半，单针预约。\n儿童接种请带接种本，成人接种请带身份证。"
                },
                "departmentWorktime":{
                    "endTime":"11:30",
                    "startTime":"08:00"
                },
                "endTime":1610467852000,
                "isUpdate":true,
                "nowTime":1610466055048,
                "subscribe":{
                    "birthday":"1996-08-02 00:00:00",
                    "cancelWay":1,
                    "createTime":"2021-01-12 23:40:52",
                    "depaCode":"4101040014",
                    "departmentVaccineId":12302,
                    "id":4295641,
                    "inoclateVerifyCode":"101509",
                    "isPay":0,
                    "isSeckill":false,
                    "isSubscribeAll":0,
                    "linkmanId":8350927,
                    "mobile":"15927037762",
                    "onlinePaymentPrice":0,
                    "serviceFee":0,
                    "status":0,
                    "subscribeDate":"2021-01-14 00:00:00",
                    "userId":9787092,
                    "userNickName":"刘香玉",
                    "vaccinePrice":35100
                },
                "subsequentEstimatedTime":[
                    {
                        "estimatedDate":"2021-02-14",
                        "vaccineIndex":"2"
                    },
                    {
                        "estimatedDate":"2021-07-14",
                        "vaccineIndex":"3"
                    }
                ],
                "vaccine":{
                    "ageEnd":45,
                    "ageStart":9,
                    "code":"8806",
                    "factoryName":"厦门万泰沧海生物技术有限公司",
                    "inoculateIndex":1,
                    "name":"二价HPV疫苗（国产）",
                    "price":35100,
                    "specifications":"0.5ml/瓶"
                }
            },
            "notOk":false,
            "ok":true
        }
    """
    # https://wx.scmttec.com/order/subscribe/clientDetail.do?id=4295641
    response = GET(cfg.URLS['ORDER_INFO'], {"id": subscribeId}, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 判断预约条件
def judge_order(departmentCode, departmentVaccineId, vaccineCode, linkmanId):
    """
    判断预约条件
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param linkmanId: 用户编号
    :return:
    {
        "code":"0000",
        "data":1,
        "notOk":false,
        "ok":true
    }
    """
    # https://wx.scmttec.com/order/subscribe/isCanSubscribe.do?depaCode=4101840004&vaccineCode=8806&id=15000
    # https://wx.scmttec.com/order/subscribe/isCanSubscribe.do?id=9708&depaCode=1101010004&vaccineCode=8803&linkmanId=8350927
    params = {
        "depaCode": departmentCode,  # 部门编码，组成：区号+区内部号
        "id": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
        "vaccineCode": vaccineCode,  # 疫苗编码
        "linkmanId": linkmanId,
    }
    response = GET(cfg.URLS['JUDGE_ORDER'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 判断是否需要注册
def judge_isNeedRegister(departmentCode, departmentVaccineId, vaccineCode, linkmanId=8350927):
    """
    判断是否需要注册
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param linkmanId: 用户编号
    :return:
    {
        "code":"0000",
        "data":1,
        "notOk":false,
        "ok":true
    }
    """
    # https://wx.scmttec.com/passport/register/isNeedRegister.do?vaccineCode=8802&depaCode=4101840002&linkmanId=8350927&departmentVaccineId=10162
    params = {
        "depaCode": departmentCode,  # 部门编码，组成：区号+区内部号
        "departmentVaccineId": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
        "vaccineCode": vaccineCode,  # 疫苗编码
        "linkmanId": linkmanId,  # 用户信息
    }
    response = GET(cfg.URLS['JUDGE_REGISTER'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 选择特定社区、特定疫苗、特定针数下可选择的日期
def workdays(departmentCode, departmentVaccineId, vaccineCode, vaccIndex, linkmanId=8350927):
    """
    选择特定社区、特定疫苗、特定针数下可选择的日期
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param vaccIndex: 选择打的第几针数，第一针，第二针，第三针
    :param linkmanId: 用户编号
    :return:
        {
            "code":"0000",
            "data":{
                "dateList":[
                    "2021-01-14",
                    "2021-01-15",
                    "2021-01-16"
                ],
                "subscribeDays":4
            },
            "notOk":false,
            "ok":true
        }
    """
    # https://wx.scmttec.com/order/subscribe/workDays.do?depaCode=4101840002&linkmanId=8350927&vaccCode=8802&vaccIndex=1&departmentVaccineId=10162
    params = {
        "depaCode": departmentCode,  # 部门编码，组成：区号+区内部号
        "linkmanId": linkmanId,  # 用户信息
        "vaccCode": vaccineCode,  # 疫苗编码
        "vaccIndex": vaccIndex,  # 选择的针数
        "departmentVaccineId": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
    }
    response = GET(cfg.URLS['CHOOSE_NUM'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 获取选择的日期中可以预约的人数
def findSubscribeAmountByDays(departmentCode, departmentVaccineId, vaccineCode, vaccIndex, days):
    """
    获取选择的日期中可以预约的人数
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param vaccIndex: 选择打的第几针数，第一针，第二针，第三针
    :param days: 查询的日期，格式为YYYYMMDD，多个时间时以“,"隔开，例如：20210114,20210115,20210116
    :return: 返回查询的每天可以预约的人数
        {
            "code":"0000",
            "data":[
                {
                    "maxSub":461,
                    "day":"20210114"
                },
                {
                    "maxSub":580,
                    "day":"20210115"
                },
                {
                    "maxSub":255,
                    "day":"20210116"
                }
            ],
            "notOk":false,
            "ok":true
        }
    """
    # https://wx.scmttec.com/order/subscribe/findSubscribeAmountByDays.do?depaCode=4101840002&vaccCode=8802&vaccIndex=1
    #       &days=20210114,20210115,20210116&departmentVaccineId=10162
    params = {
        "depaCode": departmentCode,  # 部门编码，组成：区号+区内部号
        "vaccCode": vaccineCode,  # 疫苗编码
        "vaccIndex": vaccIndex,  # 选择的针数
        "days": days,  # 选择的日期
        "departmentVaccineId": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
    }
    response = GET(cfg.URLS['GET_MAX_ORDER'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 查询某个日期下可以预约的时间点，并返回每个时间点内可以预约的人数
def departmentWorkTimes2(departmentCode, departmentVaccineId, vaccineCode, vaccIndex,
                         subscribeDate, linkmanId=8350927):
    """
    查询某个日期下可以预约的时间点，并返回每个时间点内可以预约的人数
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param vaccIndex: 选择打的第几针数，第一针，第二针，第三针
    :param subscribeDate: 查询的日期，格式为: YYYY-MM-DD
    :param linkmanId: 用户编号
    :return:
        {
            "code":"0000",
            "data":{
                "times":{
                    "code":"0000",
                    "data":[
                        {
                            "createTime":"2020-10-08 15:56:15",
                            "depaCode":"4101840004",
                            "endTime":"08:45",
                            "id":66504,
                            "maxSub":1,
                            "startTime":"08:30",
                            "tIndex":0,
                            "workdayId":12504,
                            "yn":1
                        }
                        ...
                        {}
                    ],
                    "notOk":false,
                    "ok":true
                },
                "now":1610461540543
            },
            "notOk":false,
            "ok":true
        }
    """
    # https://wx.scmttec.com/order/subscribe/departmentWorkTimes2.do?depaCode=4101840002&vaccCode=8802&vaccIndex=1
    #       &subsribeDate=2021-01-16&departmentVaccineId=10162&linkmanId=8350927
    params = {
        "depaCode": departmentCode,  # 部门编码，组成：区号+区内部号
        "vaccCode": vaccineCode,  # 疫苗编码
        "vaccIndex": vaccIndex,  # 选择的针数
        "subsribeDate": subscribeDate,  # 选择的日期,2021-01-16
        "departmentVaccineId": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
        "linkmanId": linkmanId,  # 选择预约的人
    }
    response = GET(cfg.URLS['CHOOSE_TIME_OF_DAY'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 社区编码 depaCode 中需要构造一个32位的编码字段值，防止超时提交的表单
def construct_departmentCode_32encode(subscirbeTime, now=None):
    """
    在立即预约的时候，传入的社区编号参数中不仅要传入社区编号，还有一个32位的编码字符需要构造。
    这个32位的字符我猜测认为主要是防止用户点进去提交的界面后，两分钟之内如果没有提交则会过时，需要用户重新再次进去提交界面
    depaCode=4101840004_4a4eccf02eda431817ae943d22d8bbc0
    后面的4a4eccf02eda431817ae943d22d8bbc0这个数据没找到怎么生成的，估计是md5加密了，
    看了js有这一段代码：
        depaCode: this.submitInfo.department.code + "_" +
                f()(moment(new Date(this.submitInfo.nowTime)).format("YYYYMMDDHHmm") + this.submitInfo.subscirbeTime.value + this.abcde)
    :param subscirbeTime: 选择的时间段，是编码过的时间段，具体可以参考 departmentWorkTimes2 返回的每一个时间段的 id 字段的值
    :return: 返回构造的32位编码字符
    """
    end = 'fuckhacker10000times'
    # 中间一步，构造编码的时间 depaCode=4101840004_4a4eccf02eda431817ae943d22d8bbc0
    cur_time = get_server_time()  # 2021-01-14 16:37:10
    cur_time = get_server_time_miaomiao()
    # self._header['st'] = hashlib.md5(str(cur_time).encode('utf-8')).hexdigest()
    # print("cur_time: ", cur_time)
    # print("subscirbeTime id: ", subscirbeTime)
    decodetime = cur_time.replace('-', '').replace(' ', '').replace(':', '')[0:12] + str(subscirbeTime) + end
    # decodetime = cur_time + str(subscirbeTime) + end
    # decodetime = str(now) + str(subscirbeTime) + end
    depaCode_md5 = hashlib.md5(str(decodetime).encode('utf-8')).hexdigest()
    # depaCode_md5 = hashlib.md5((depaCode_md5+'ux$ad70*b').encode('utf-8')).hexdigest()
    print("decodetime_ori: ", decodetime)
    print("depaCode_md5: ", depaCode_md5)
    return depaCode_md5


# 开始预约
def startOrder(departmentCode, departmentVaccineId, vaccineCode, vaccIndex, subscribeDate, subscirbeTime,
               linkmanId=8350927, now=None):
    """
    立即预约
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param vaccIndex: 选择打的第几针数，第一针，第二针，第三针
    :param subscribeDate: 查询的日期，格式为: YYYY-MM-DD
    :param subscirbeTime: 选择的时间段，是编码过的时间段，具体可以参考 departmentWorkTimes2 返回的每一个时间段的 id 字段的值
    :param linkmanId: 用户编号
    :return:
    预约成功的返回结果信息
        {
            "code":"0000",
            "data":{
                "subscribeId":4295641
            },
            "notOk":false,
            "ok":true
        }
    """
    # 第七步，选择时间之后，开始预约
    # https://wx.scmttec.com/order/subscribe/add.do?
    #   vaccineCode=8806&vaccineIndex=1&linkmanId=8350927&subscribeDate=2021-01-13
    #   &subscirbeTime=66505&departmentVaccineId=15000
    #   &depaCode=4101840004_4a4eccf02eda431817ae943d22d8bbc0&serviceFee=0
    # depaCode_md5='090ce172dbb4e8f5ac4cdc315922532c'
    depaCode_md5 = construct_departmentCode_32encode(subscirbeTime=subscirbeTime, now=now)
    params = {
        "vaccineCode": vaccineCode,  # 疫苗编码
        "vaccineIndex": vaccIndex,  # 选择的针数
        "linkmanId": linkmanId,  # 选择预约的人
        "subscribeDate": subscribeDate,  # 选择的日期
        "subscirbeTime": subscirbeTime,  # 选择的时间,上面选择某一天日期获得的时间id
        "departmentVaccineId": departmentVaccineId,  # 部门疫苗id，也就是选择请求某一个医院的唯一标识
        "depaCode": str(departmentCode) + '_' + depaCode_md5,  # 部门编码，
        "serviceFee": 0,  # 部门编码，组成：区号+区内部号
    }
    print('[info]: 预约日期为：{}'.format(subscribeDate))
    response = GET(cfg.URLS['START_ORDER'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


# 根据所有可预约的日期，依次选择每一天的每一个时间段去预约，直到有一个时间段预约成功或者全部的时间段都尝试预约结束
def loop_order_until_success(departmentCode, departmentVaccineId, vaccineCode, vaccIndex, subscribeDates,
                             linkmanId=8350927):
    """
    根据所有可预约的日期，依次选择每一天的每一个时间段去预约，直到有一个时间段预约成功或者全部的时间段都尝试预约结束，才返回
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :param vaccIndex: 选择打的第几针数，第一针，第二针，第三针
    :param linkmanId: 用户编号
    :param subscribeDates: 可预约的日期和对应的日期内可预约的人数
        [
            {
                "maxSub":461, "day":"20210114"
            },
            {
                "maxSub":580, "day":"20210115"
            },
            {
                "maxSub":255, "day":"20210116"
            }
        ]
    :return:    预约成功返回： True, { "subscribeId":4295641 },（预约编号，可以通过该预约编号查询详细的预约信息）
                预约失败返回： False, None
    """
    sleep_time = 2.67
    for date in subscribeDates:
        maxSub = date['maxSub']
        subscribeDate = date['day']
        print('[info]: 日期 {} 可以预约人数为 {}'.format(subscribeDate, maxSub))
        if maxSub <= 0:
            # 改日期可预约人数为0，则继续判断下一天
            continue

        # 该天可预约人数不为0，选择某一个时间段预约，即获取该天的每一个时间段可预约的人数信息
        subscribeDate = subscribeDate[0:4] + '-' + subscribeDate[4:6] + '-' + subscribeDate[6:8]
        response = departmentWorkTimes2(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                                        vaccineCode=vaccineCode, vaccIndex=vaccIndex, subscribeDate=subscribeDate,
                                        linkmanId=linkmanId)
        if response is None:
            continue
        if not response['ok']:
            # 请求该天的每一个时间段可预约人数失败！
            print('[error]: 针数: {}, 日期: {}不可预约, {}'.format(cfg.vaccIndex, subscribeDate, response['msg']))
            continue

        # 成功请求到该天的每一个时间段可预约人数
        data = response['data']  # keys : [ times, now ]
        now = data['now']
        times = data['times']  # 该天的每一个时间段可预约人数详细信息
        if not times['ok']:
            # 获取该天的每一个时间段的可预约人数信息失败！
            print('[error]: 获取时间点有误, {}'.format(response['msg']))
            continue

        # 成功获取该天的每一个时间段可预约的人数信息
        # list : [ {createTime, depaCode, endTime, id, maxSub, startTime, tIndex, workdayId, yn  } ... { } ]
        times_data = times['data']

        # 循环判断该日期 subscribeDate 内的每个时间段信息，尝试进行预约，预约成功即返回退出
        times_length = len(times_data)
        current_time_index = 0
        # for time in times_data:
        while current_time_index < times_length:
            """
            {
                "createTime":"2020-10-08 15:56:15",
                "depaCode":"4101840004",
                "endTime":"08:45",
                "id":66504,
                "maxSub":1,
                "startTime":"08:30",
                "tIndex":0,
                "workdayId":12504,
                "yn":1
            }
            """
            # print('test1')
            time = times_data[current_time_index]
            current_time_index += 1  # 下一个时间段
            if time['maxSub'] <= 0:
                # 该时间段可预约人数为0，跳过该时间段，继续判断下一个时间段
                continue
            subscirbeTime = time['id']

            print('[info]: 日期 {}, 时间段 {} - {}, 时间段编号 {}, 可预约的人数为 {}'
                  .format(subscribeDate, time['startTime'], time['endTime'], time['id'], time['maxSub']))

            # 第七步，选择时间之后，开始预约
            response = startOrder(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                                  vaccineCode=vaccineCode,
                                  vaccIndex=cfg.vaccIndex, subscribeDate=subscribeDate, subscirbeTime=subscirbeTime,
                                  linkmanId=linkmanId, now=now)
            if response is None:
                continue
            if not response['ok']:
                print('[error]: 日期 {}, 时间段 {} - {}, 预约失败， {}'
                      .format(subscribeDate, time['startTime'], time['endTime'], response['msg']))

                # {"code":"3101","msg":"太多的重复请求!","notOk":true,"ok":false}
                # {"code":"1101","msg":"下单操作频繁,请稍后再试吧!","notOk":true,"ok":false}
                code = response['code']
                if code == "1101" or code == "3101":
                    sleep_time += 0.01
                    # 当前请求没有请求成功，所以重新请求当前时间段
                    current_time_index -= 1
                    print('当前睡眠时间为：', sleep_time)
                #     print(sysTime.ctime())
                #     sysTime.sleep(3)
                #     print(sysTime.ctime())

                # 为了防止频繁下单导致失败，这里系统睡眠一段时间
                # print('当前睡眠时间为：', sleep_time)
                sysTime.sleep(sleep_time)

                print()
                print()
                continue
            else:
                print('[info]: 预约成功')
                return True, response['data']  # { "subscribeId":4295641 }

    return False, None


def check_order_number(departmentCode, departmentVaccineId, linkmanId=8350927, username=None):
    #####################################################################
    # 如果用户名不为空，根据传入的用户名来获取 linkmanId
    if username is not None:
        linkmanId = get_linkmanId_by_name(username)
        if linkmanId is None:
            print('[error]: 输入的用户名 {} 没有在系统中注册'.format(username))
            return 0
    #####################################################################

    #####################################################################
    # 根据社区疫苗编号获取该社区的信息，从而获取到该社区是预约哪一价的疫苗，机获取疫苗编号 vaccineCode
    response = get_department_vaccine_info(depaVaccId=departmentVaccineId)
    if response is None:
        return 0
    if not response['ok']:
        print('[error]: 没有找到该社区的信息... , {}'.format(response['msg']))
        return 0
    departmentName = response['data']['departmentName']
    vaccineCode = response['data']['vaccineCode']
    #####################################################################

    #####################################################################
    # 第一步，判断是否可预约
    # https://wx.scmttec.com/order/subscribe/isCanSubscribe.do?depaCode=4101840002&vaccineCode=8802&id=10162
    response = judge_order(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                           vaccineCode=vaccineCode, linkmanId=linkmanId)
    if response is None:
        return 0
    if not response['ok']:
        # print(response)
        print('[error]: 没有可预约的疫苗... , {}'.format(response.get('msg', 'error_info')))
        return 0
    if response['data'] == 0:
        print('[error]: 该社区暂时没有可预约信息...')
        return 0
    #####################################################################

    #####################################################################
    # 第二步，获取疫苗信息
    # https://wx.scmttec.com/base/department/vaccine.do?vaccineCode=8802&depaCode=4101840002&departmentVaccineId=10162&isShowDescribtion=false
    response = get_vaccine_info(depaCode=departmentCode, depaVaccId=departmentVaccineId, vaccineCode=vaccineCode)

    response = get_server_time()
    #####################################################################

    #####################################################################
    # 第三步，判断是否需要注册
    # https://wx.scmttec.com/passport/register/isNeedRegister.do?vaccineCode=8802&depaCode=4101840002&linkmanId=8350927&departmentVaccineId=10162
    # response = judge_isNeedRegister(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
    #                                 vaccineCode=vaccineCode, linkmanId=linkmanId)
    # if response is None:
    #     return 0
    # if not response['ok'] or response['data'] == 0:
    #     print('[error]: 需要注册..., response : ', response)
    #     # print(response)
    #     return 0
    #####################################################################

    #####################################################################
    # 第四步，选择针数
    # https://wx.scmttec.com/order/subscribe/workDays.do?depaCode=4101840002&linkmanId=8350927&vaccCode=8802&vaccIndex=1&departmentVaccineId=10162
    response = workdays(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId, vaccineCode=vaccineCode,
                        vaccIndex=cfg.vaccIndex, linkmanId=linkmanId)
    if response is None:
        return 0
    if not response['ok']:
        print('[error]: 针数 {} 没有可预约日期, {}'.format(cfg.vaccIndex, response['msg']))
        return 0
    #####################################################################

    #####################################################################
    # 第五步，同时获取每一天的可预约的人数
    dataList = [d.replace('-', '') for d in response['data']['dateList']]
    days = ','.join(dataList)
    response = findSubscribeAmountByDays(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                                         vaccineCode=vaccineCode,
                                         vaccIndex=cfg.vaccIndex, days=days)
    if response is None:
        return 0
    if not response['ok']:
        print('[error]: 针数: {}, 日期: {}不可预约, {}'.format(cfg.vaccIndex, days, response['msg']))
        return 0

    subscribeDates = response['data']
    if len(subscribeDates) == 0:
        print('[error]: 可订阅天数为0...')
        return 0

    for sub_data in subscribeDates:
        # "maxSub":461, "day":"20210114"
        maxSub = sub_data['maxSub']
        date = sub_data['day']
        print('日期：{}可预约人数：{}'.format(date, maxSub))
        if maxSub != 0:
            # TODO 发送短信提示，该日期可以预约
            print('日期：{}可预约人数：{}'.format(date, maxSub))
            if len(departmentName) > 12:
                departmentName = departmentName[0:12]
            # print(departmentName)
            send_text_message([departmentName, str(maxSub)])
            return subscribeDates
    return 0


# 某一个医院界面内点击立即预约按钮
def order_immediately(departmentCode, departmentVaccineId, linkmanId=8350927, username=None):
    """
    某一个医院界面内点击立即预约按钮
        请求参数组成：depaCode=4201020003&vaccineCode=8803&id=3680
    :param username: 开始预约的用户名字，当该字段不为空时，它将覆盖传入的 linkmanId 参数
    :param departmentCode: 部门编码，组成：区号+区内部号
    :param departmentVaccineId: 部门疫苗id，也就是选择请求某一个医院的唯一标识。注意：虽然可能是同一个社区名字，但是预约的价数不一样，则对应的 departmentVaccineId 也不一样
    :param linkmanId: 用户编号
    :return: 返回请求的返回结果:
                预约成功，返回：get_my_order_info_by_subscribeId 函数返回的结果，即预约成功的详细信息
                预约失败，返回 None
    """

    #####################################################################
    # 如果用户名不为空，根据传入的用户名来获取 linkmanId
    if username is not None:
        linkmanId = get_linkmanId_by_name(username)
        if linkmanId is None:
            print('[error]: 输入的用户名 {} 没有在系统中注册'.format(username))
            return 0
    #####################################################################

    #####################################################################
    # 根据社区疫苗编号获取该社区的信息，从而获取到该社区是预约哪一价的疫苗，机获取疫苗编号 vaccineCode
    response = get_department_vaccine_info(depaVaccId=departmentVaccineId)
    if response is None:
        return
    if not response['ok']:
        print('[error]: 没有找到该社区的信息... , {}'.format(response['msg']))
        return
    departmentName = response['data']['departmentName']
    vaccineCode = response['data']['vaccineCode']
    #####################################################################

    #####################################################################
    # 第一步，判断是否可预约
    # https://wx.scmttec.com/order/subscribe/isCanSubscribe.do?depaCode=4101840002&vaccineCode=8802&id=10162
    response = judge_order(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                           vaccineCode=vaccineCode, linkmanId=linkmanId)
    if response is None:
        return
    if not response['ok']:
        # print(response)
        print('[error]: 没有可预约的疫苗... , {}'.format(response.get('msg', 'error_info')))
        return
    if response['data'] == 0:
        print('[error]: 该社区暂时没有可预约信息...')
        return
    #####################################################################

    #####################################################################
    # 第二步，获取疫苗信息
    # https://wx.scmttec.com/base/department/vaccine.do?vaccineCode=8802&depaCode=4101840002&departmentVaccineId=10162&isShowDescribtion=false
    response = get_vaccine_info(depaCode=departmentCode, depaVaccId=departmentVaccineId, vaccineCode=vaccineCode)

    response = get_server_time()
    #####################################################################

    #####################################################################
    # 第三步，判断是否需要注册
    # https://wx.scmttec.com/passport/register/isNeedRegister.do?vaccineCode=8802&depaCode=4101840002&linkmanId=8350927&departmentVaccineId=10162
    # response = judge_isNeedRegister(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
    #                                 vaccineCode=vaccineCode, linkmanId=linkmanId)
    # if response is None:
    #     return
    # if not response['ok'] or response['data'] == 0:
    #     print('[error]: 需要注册...')
    #     print(response)
    #     return
    #####################################################################

    #####################################################################
    # 第四步，选择针数
    # https://wx.scmttec.com/order/subscribe/workDays.do?depaCode=4101840002&linkmanId=8350927&vaccCode=8802&vaccIndex=1&departmentVaccineId=10162
    response = workdays(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId, vaccineCode=vaccineCode,
                        vaccIndex=cfg.vaccIndex, linkmanId=linkmanId)
    if response is None:
        return
    if not response['ok']:
        print('[error]: 针数 {} 没有可预约日期, {}'.format(cfg.vaccIndex, response['msg']))
        return
    #####################################################################

    #####################################################################
    # 第五步，同时获取每一天的可预约的人数
    dataList = [d.replace('-', '') for d in response['data']['dateList']]
    days = ','.join(dataList)
    response = findSubscribeAmountByDays(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                                         vaccineCode=vaccineCode,
                                         vaccIndex=cfg.vaccIndex, days=days)
    if response is None:
        return
    if not response['ok']:
        print('[error]: 针数: {}, 日期: {}不可预约, {}'.format(cfg.vaccIndex, days, response['msg']))
        return

    subscribeDates = response['data']
    if len(subscribeDates) == 0:
        print('[error]: 可订阅天数为0...')
        return

    # 遍历所有的时间段，直到预约成功
    flag, response = loop_order_until_success(departmentCode=departmentCode, departmentVaccineId=departmentVaccineId,
                                              vaccineCode=vaccineCode,
                                              vaccIndex=cfg.vaccIndex, subscribeDates=response['data'],
                                              linkmanId=linkmanId)
    if response is None:
        return

    if flag:
        subscribeId = response['subscribeId']
        response = get_my_order_info_by_subscribeId(subscribeId=subscribeId)
        save_json(response, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                     'order_success.json'))
        print_my_order_success_info(data=response)
    else:
        print('[error]: 所有全部预约失败！')

    return response
