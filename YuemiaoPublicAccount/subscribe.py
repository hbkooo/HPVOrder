# encoding: utf-8
"""
开始订阅某个社区时的操作
"""
from YuemiaoPublicAccount.util import *
from YuemiaoPublicAccount.vaccine import get_vaccine_info
from YuemiaoPublicAccount.linkman import check_linkman
from YuemiaoPublicAccount.all_city_code import save_all_city_info
from YuemiaoPublicAccount.department_info import get_all_departments
from YuemiaoPublicAccount.linkman import get_linkmanId_by_name
import YuemiaoPublicAccount.config as cfg


def get_all_my_subscribe():
    """
    获取用户所有的订阅信息
    :return:
    {
        "code":"0000",
        "data":{
            "end":98,
            "limit":500,
            "offset":0,
            "pageListSize":9,
            "pageNumList":[
                1
            ],
            "pageNumber":1,
            "pages":1,
            "rows":[
                {
                    "depaCode":"5001020005",
                    "id":23377523,
                    "ineffective":0,
                    "isNotice":0,
                    "linkmanId":8350927,
                    "name":"刘香玉",
                    "rankingRange":"重庆市涪陵区敦仁街道社区卫生服务中心",
                    "regionCode":"500102",
                    "registerTime":"2021-01-14 15:18:44",
                    "registerType":1,
                    "status":1,
                    "vaccineCode":"8803",
                    "vaccineName":"九价HPV疫苗（进口）"
                },
                {
                    "depaCode":"4109020002",
                    "id":23305154,
                    "ineffective":0,
                    "isNotice":0,
                    "linkmanId":8350927,
                    "name":"刘香玉",
                    "rankingRange":"濮阳市疾控中心预防接种门诊",
                    "regionCode":"410902",
                    "registerTime":"2021-01-12 19:28:15",
                    "registerType":1,
                    "status":1,
                    "vaccineCode":"8803",
                    "vaccineName":"九价HPV疫苗（进口）"
                },
                ...
                {}
            ],
            "total":99
        },
        "notOk":false,
        "ok":true
    }
    """
    # https://wx.scmttec.com/passport/register/myRegisterList.do?offset=0&limit=5

    params = {'offset': 0, 'limit': 10}
    response = GET(cfg.URLS['ALL_SUBSCRIBE'], params, headers=cfg.REQ_HEADERS, verify=False)

    total = response['data']['total']
    if params['limit'] < total:
        params['limit'] = total
        print(params)
        response = GET(cfg.URLS['ALL_SUBSCRIBE'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


def get_my_subscribe_info_by_registerDetailId(registerDetailId):
    """
    根据订阅的id编号查找订阅信息
    :param registerDetailId: 订阅成功返回的id编号
    :return: 查询的订阅信息
    当订阅成功时返回的该订阅的详细信息：https://wx.scmttec.com/passport/register/registerRanking.do?registerDetailId=23377523
    {
        "code":"0000",
        "data":{
            "depaCode":"5001020005",
            "id":23377523,
            "isOldRegister":0,
            "isSubOnlySubscriber":1,
            "rankingNumber":10394,
            "rankingRange":"重庆市涪陵区敦仁街道社区卫生服务中心",
            "regionCode":"50",
            "registerTime":"2021-01-14 15:18:44",
            "registerType":1,
            "status":1,
            "vaccineCode":"8803",
            "vaccineName":"九价HPV疫苗（进口）"
        },
        "notOk":false,
        "ok":true
    }
    从我的订阅里面点击查看某一个订阅：https://wx.scmttec.com/passport/register/myRegisterItem.do?registerDetailId=23377523
    {
        "code":"0000",
        "data":{
            "depaCode":"5001020005",
            "depaName":"重庆市涪陵区敦仁街道社区卫生服务中心",
            "id":23377523,
            "ineffective":0,
            "isNotice":0,
            "isShowTime":0,
            "isSubOnlySubscriber":1,
            "linkmanId":8350927,
            "name":"刘香玉",
            "registerTime":"2021-01-14 15:18:44",
            "registerType":0,
            "status":1,
            "vaccineCode":"8803",
            "vaccineName":"九价HPV疫苗（进口）"
        },
        "notOk":false,
        "ok":true
    }
    """
    # https://wx.scmttec.com/passport/register/registerRanking.do?registerDetailId=23300858
    # https://wx.scmttec.com/passport/register/myRegisterItem.do?registerDetailId=23379350
    # response = GET(cfg.URLS['SUBSCRIBE_INFO_RANK'], {"registerDetailId": registerDetailId},
    #                headers=cfg.REQ_HEADERS, verify=False)
    response = GET(cfg.URLS['SUBSCRIBE_INFO'], {"registerDetailId": registerDetailId},
                   headers=cfg.REQ_HEADERS, verify=False)
    return response


def delete_subscribe(registerDetailId):
    """
    根据订阅成功的编号取消订阅
    :param registerDetailId: 订阅成功时返回的编号
    :return:
    {
        "code":"0000",
        "data":true,
        "notOk":false,
        "ok":true
    }
    """
    # GET https://wx.scmttec.com/passport/register/delete.do?registerDetailId=23379350
    response = GET(cfg.URLS['SUBSCRIBE'], {'registerDetailId': registerDetailId}, headers=cfg.REQ_HEADERS, verify=False)
    return response


def subscribe(depaCode, depaVaccId, linkmanId, vaccineCode=8803):
    """
    在某个部门发起订阅
    :param depaCode: 区域编码
    :param depaVaccId: 部门疫苗id，医院唯一标识
    :param vaccineCode: 疫苗编号
    :param linkmanId: 应该是用户编号，应该是固定的，抓包没找到哪里有这个数据
    :return:    订阅失败：False, -1
                订阅成功：True, registerDetailId(订阅注册的id)
    """

    # print()
    # print('='*50)
    # print('subscribe')

    # 第一步，获取疫苗产品id
    response = get_vaccine_info(depaCode=depaCode, depaVaccId=depaVaccId, vaccineCode=vaccineCode)
    # print('第一步获取产品信息 response', response)
    if not response['ok']:
        print('[error]: ', response['msg'])
        return False, -1

    # 第二步，信息check检查
    productId = response['data']['productId']
    response = check_linkman(depaCode=depaCode, depaVaccId=depaVaccId, productId=productId, linkmanId=linkmanId,
                             vaccineCode=vaccineCode)
    # print('第二步检查信息 response', response)
    if not response['ok'] or not response['data']:
        print('[error]: ', response['msg'])
        return False, -1

    # 第三步，开始订阅
    # https://wx.scmttec.com/passport/register/subscibe.do?vaccineCode=8803&depaCode=3101150013&linkmanId=8350927
    #   &depaVaccId=13086&productId=128
    # print(response)
    params = {
        'depaCode': depaCode,
        'depaVaccId': depaVaccId,
        'vaccineCode': vaccineCode,
        'productId': productId,
        'linkmanId': linkmanId
    }
    response = GET(cfg.URLS['SUBSCRIBE'], params, headers=cfg.REQ_HEADERS, verify=False)

    """
        {
            "code":"0000",
            "data":23377523,
            "notOk":false,
            "ok":true
        }
    """
    # print('第三步开始订阅 response', response)

    if response['ok']:
        print('[info]: 订阅成功，订阅编号id为', response['data'])
    else:
        print('[info]: 订阅失败，', response['msg'])
        return False, -1
    # print('='*50)
    # print()
    return True, response['data']


def subscribe_by_region_id(regionCode, linkmanId=8350927, username=None):
    """
    根据区域id依次订阅该区域内的所有医院
    :param username: 根据用户名来更新 linkmanId
    :param regionCode: 区域编号
    :param linkmanId: 订阅的用户的编号
    :return: 订阅成功的数量
    """
    if username is not None:
        linkmanId = get_linkmanId_by_name(username)
        if linkmanId is None:
            print('[error]: 输入的用户名 {} 没有在系统中注册'.format(username))
            return 0

    departments = get_all_departments(regionCode)
    count = 0
    for department in departments:
        departmentCode = department['code']
        depaVaccId = department['depaVaccId']
        vaccineCode = department['vaccineCode']
        flag, registerDetailId = subscribe(depaCode=departmentCode, depaVaccId=depaVaccId, vaccineCode=vaccineCode, linkmanId=linkmanId)
        if flag:
            count += 1
    return count


def subscribe_by_province(province):
    """
    根据省的名字订阅全省可订阅的社区医院
    :param province: 省名字
    :return: count,成功订阅的数量
    """
    p_json = osp.join(cfg.save_city_code_root, province + '.json')
    if not osp.exists(p_json):
        if osp.exists(osp.join(cfg.save_city_code_root, 'provinces.json')):
            f = open(osp.join(cfg.save_city_code_root, 'provinces.json'), encoding='utf-8')
            provinces = json.load(f)
            f.close()
            if province not in provinces.keys():
                print('[error]: 你输入的省份"{}"不在已知的所有省份 {} 中'.format(province, provinces.keys()))
                return
        else:
            save_all_city_info()
    if not osp.exists(p_json):
        provinces = os.listdir(cfg.save_city_code_root)
        provinces = [p.split('.')[0] for p in provinces]
        provinces.remove('provinces')
        print('[error]: 你输入的省份"{}"不在已知的所有省份 {} 中'.format(province, provinces))
        return
    count = 0
    linkmanId = get_linkmanId_by_name(cfg.username)
    if linkmanId is None:
        print('[error]: 配置文件 config.py 中输入的用户名(username) {} 没有在系统中注册'.format(cfg.username))
        return

    with open(p_json, encoding='utf-8') as f:
        cities = json.load(f)
        for city in cities:
            if 'area' not in cities[city]:
                print("[info]: 处理直辖市{}的{}".format(province, city))
                regionCode = cities[city]
                count += subscribe_by_region_id(regionCode=regionCode, linkmanId=linkmanId)
            else:
                print('[info]: 处理城市：{}...'.format(city))
                areas = cities[city]['area']
                for area in areas:
                    print('\t[info]: 处理 {} 的 {}...'.format(city, area))
                    regionCode = areas[area]
                    count += subscribe_by_region_id(regionCode=regionCode, linkmanId=linkmanId)
    print('[info]: 一共成功订阅 {} 个社区医院'.format(count))
    return count
