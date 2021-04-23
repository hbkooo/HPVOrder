# encoding: utf-8
"""
用户信息操作
"""
from YuemiaoPublicAccount.util import *
import YuemiaoPublicAccount.config as cfg


# 获取系统中所有的用户信息
def get_all_users():
    """
    获取系统中所有的用户信息
    :return:
    {
        "code":"0000",
        "data":[
            {
                "address":"",
                "birthday":"1996-08-02 00:00:00",
                "createTime":"2021-01-06 13:14:05",
                "id":8350927,                           # linkmanId
                "idCardNo":"",
                "isDefault":1,
                "modifyTime":"2021-01-06 13:14:05",
                "name":"刘香玉",
                "regionCode":"410104",
                "relationType":1,
                "sex":2,
                "userId":9787092,
                "yn":1
            },
            {
                "address":"",
                "birthday":"1997-10-23 00:00:00",
                "createTime":"2021-01-12 19:33:27",
                "id":8443813,                           # linkmanId
                "idCardNo":"",
                "isDefault":0,
                "modifyTime":"2021-01-12 19:33:27",
                "name":"韩冰凯",
                "regionCode":"420111",
                "relationType":6,
                "sex":1,
                "userId":9787092,
                "yn":1
            }
        ],
        "notOk":false,
        "ok":true
    }
    """
    # https://wx.scmttec.com/order/linkman/findByUserId.do
    response = GET(cfg.URLS['ALL_USER'], headers=cfg.REQ_HEADERS, verify=False)
    return response


# 根据用户输入的名字查询该用户的 linkmanId
def get_linkmanId_by_name(query_name):
    """
    根据用户输入的名字查询该用户的 linkmanId
    :param query_name: 用户查询的名字
    :return: 如果找到返回用户的 linkmanId；否则返回 None
    """
    response = get_all_users()
    if not response['ok']:
        print('[error]: 获取用户信息失败：{}'.format(response.get('msg', 'error')))
        exit()
        # return None
    data = response['data']
    if len(data) == 0:
        print('[error]: 当前系统中还没有添加用户信息...')
        return None
    items = {item['name']: item['id'] for item in data}
    if query_name not in items:
        print('[error]: 当前系统中所有用户为 {}, 暂时没有添加用户 {}'.format(items.keys(), query_name))
        return None
    return items[query_name]


# 信息check检查，检测; 在订阅时用到这个检查
def check_linkman(depaCode, depaVaccId, productId, linkmanId=8350927, vaccineCode=8803):
    """
    信息check检查，检测; 在订阅时用到这个检查
    :param depaCode: 区域编码
    :param depaVaccId: 部门疫苗id，医院唯一标识
    :param productId: 产品id
    :param linkmanId: 用户的相关的id
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :return:
    {
        "code":"0000",
        "data":true,
        "notOk":false,
        "ok":true
    }
    or
    {
        "code":"9999",
        "msg":"您在本门诊已订阅该疫苗的“到苗通知”，请勿重复订阅",
        "notOk":true,
        "ok":false
    }
    """
    # GET https://wx.scmttec.com/passport/register/checkLinkman.do?vaccineCode=8803&depaCode=4201020003&linkmanId
    #   =8350927&depaVaccId=3680&productId=128
    params = {
        'depaCode': depaCode,
        'depaVaccId': depaVaccId,
        'vaccineCode': vaccineCode,
        'productId': productId,
        'linkmanId': linkmanId
    }
    response = GET(cfg.URLS['SUBSCRIBE_CHECK'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response
