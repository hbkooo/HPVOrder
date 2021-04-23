# encoding: utf-8
"""
有关社区信息的操作
"""

import xlwt
import pandas
from YuemiaoPublicAccount.util import *
import YuemiaoPublicAccount.config as cfg
from YuemiaoPublicAccount.all_city_code import save_all_provinces


#######################################################################################################
#######################################################################################################
#######################################################################################################
# 社区疫苗信息操作，可以查看是否已经到了疫苗
# 根据部门疫苗编号id获取该医院的信息，（即模拟的是点击某一个医院后的返回消息）
def get_department_vaccine_info(depaVaccId):
    """
    根据部门疫苗编号id获取该医院的信息，（即模拟的是点击某一个医院后的返回消息）
    :param depaVaccId: 请求的部门疫苗编号id
    :return: 返回该医院的详细信息
    {
        code: '0000'
        data: {
            id: 10164                           # depaVaccId,部门疫苗编号id
            departmentCode: 4101840002          # 部门编号
            vaccineCode: 8803                   # 疫苗编号
            departmentName: 新郑市龙湖镇卫生院（新郑市第三人民医院）            # 部门名字
            describtion:                # 描述
            instructionsUrls: []                # 说明网址
            isArriveVaccine: 0                  # 是否到达疫苗
            name: 九价HPV疫苗（仅接受第一针在我门诊接种的，并该接种第二针、第三针的受种者）...
            prompt:                             # 提示，弹窗提示消息
            subscribed: 13                      # 已订阅
            total: -1                           # 总数
            stopSubscribe: 1                    # 停止订阅
            sourceType: 1                       # 源类型
            urls: [ *.jpg ... *.jpg]            # 图片链接
            items: [
                {
                    id: 10164                   # depaVaccId,部门疫苗编号id
                    vaccineCode: 8803           # 疫苗编号
                    factoryName: 默沙东集团       # 工厂名称
                    specifications: 0.5mL/支     # 规格
                    name:                       # 疫苗名字描述
                    price: 132000               # 价格
                    sourceType: 1               # 源类型
                    isNoticedUserAllowed: 0     # 是否通知用户允许
                }
            ]
            departmentVaccineId: 10164          # 部门疫苗id
            isNoticedUserAllowed: 0             #
        }
        ok: 'true'
    }
    """
    # https://wx.scmttec.com/base/departmentVaccine/item.do?id=7259&isShowDescribtion=true&showOthers=true
    params = {'id': depaVaccId, 'isShowDescribtion': True, 'showOthers': True}
    res = GET(cfg.URLS['DEPARTMENT'], params, headers=cfg.REQ_HEADERS, verify=False)
    name = res.get('departmentName', str(depaVaccId))
    # print('get_department_vaccine_info, name : ', name)
    return res


# 根据区域编号查找该区域所有的社区疫苗信息
def get_all_department_vaccine_infos(regionCode):
    """
    根据区域编号查找该区域所有的社区疫苗信息
    :param regionCode:
    :return: [ departmentVaccine1, departmentVaccine2, ..., departmentVaccine ... ]
    departmentVaccine: {
            id: 10164                           # depaVaccId,部门疫苗编号id
            departmentCode: 4101840002          # 部门编号
            vaccineCode: 8803                   # 疫苗编号
            departmentName: 新郑市龙湖镇卫生院（新郑市第三人民医院）            # 部门名字
            describtion:                # 描述
            instructionsUrls: []                # 说明网址
            isArriveVaccine: 0                  # 是否到达疫苗
            name: 九价HPV疫苗（仅接受第一针在我门诊接种的，并该接种第二针、第三针的受种者）...
            prompt:                             # 提示，弹窗提示消息
            subscribed: 13                      # 已订阅
            total: -1                           # 总数
            stopSubscribe: 1                    # 停止订阅
            sourceType: 1                       # 源类型
            urls: [ *.jpg ... *.jpg]            # 图片链接
            items: [
                {
                    id: 10164                   # depaVaccId,部门疫苗编号id
                    vaccineCode: 8803           # 疫苗编号
                    factoryName: 默沙东集团       # 工厂名称
                    specifications: 0.5mL/支     # 规格
                    name:                       # 疫苗名字描述
                    price: 132000               # 价格
                    sourceType: 1               # 源类型
                    isNoticedUserAllowed: 0     # 是否通知用户允许
                }
            ]
            departmentVaccineId: 10164          # 部门疫苗id
            isNoticedUserAllowed: 0             #
        }
    """
    print('#' * 50)
    print('查询社区疫苗信息...')
    departments = get_all_departments(regionCode=regionCode)

    departmentVaccineInfos = []
    for department in departments:
        depaVaccId = department['depaVaccId']
        departmentVaccineInfo = get_department_vaccine_info(depaVaccId=depaVaccId)
        if not departmentVaccineInfo['ok']:
            print('[warning]: 获取社区医院“{}”失败'.format(department['name']))
            continue
        info = departmentVaccineInfo['data']
        departmentVaccineInfos.append(info)
    return departmentVaccineInfos


#######################################################################################################
#######################################################################################################
#######################################################################################################
# 社区信息操作，可以查看是否有秒杀，好像发布的信息不太准确
# 通过社区名字在全国范围内搜索来获取社区信息，支持模糊查找，即直接输入一个关键词，查找到所有包含该关键词的社区医院
def get_department_by_name(name):
    """
    通过社区名字来获取社区信息;搜索全国范围内的该社区名称
    :param name: 社区名字
    :return: [ hospital1 hospital2 ... ]
    hospital: {
                code: ''            # departmentCode，部门代码
                name: ''            # 名称
                imgUrl: ''          # 图片链接
                regionCode: ''      # 该医院所属地区编号
                address: ''         # 医院地址
                tel:''              # 医院电话
                isOpen: ''          # 是否开放
                latitude:''         # 经度
                longitude: ''       # 纬度
                worktimeDesc: ''    # 工作时间描述
                distance: ''        # 距离
                vaccineCode: ''     # 疫苗编号
                vaccineName: ''     # 疫苗名称
                total: ''           # 总数
                isSeckill: ''       # 是否秒杀
                price: ''           # 价格
                sourceType: ''      #
                isHiddenPrice: ''   #
                depaCodes: ''       # 部门编码
                vaccines: ''        # 疫苗
                depaVaccId: ''      # 部门疫苗id，重要重要重要！！！！请求某一个医院的信息时用到这个字段
                stopSubscribe: ''   # 停止订阅
            }
    """
    # 　https://wx.scmttec.com/base/department/getDepartments.do
    params = {
        'customId': cfg.customId,  # 3-九价疫苗；2-四价疫苗；1-二价疫苗
        'limit': 500,  # 请求的医院最大数目
        'isOpen': 1,
        'sortType': 1,
        # 'vaccineCode': 0,             # 疫苗编号
        'offset': 0,
        'name': name,  # 医院名字
        'longitude': 0,  # 经度
        'latitude': 0,  # 纬度
    }
    res = GET(cfg.URLS['ALL_DEPARTMENTS'], params, headers=cfg.REQ_HEADERS, verify=False)

    total = res['data']['total']
    if params['limit'] < total:
        params['limit'] = total
        print(params)
        res = GET(cfg.URLS['ALL_DEPARTMENTS'], params, headers=cfg.REQ_HEADERS, verify=False)
    # print(res)
    departments = res['data']['rows']
    if len(departments) == 0:
        # print('[error]: 您输入的社区名字"{}"暂时没有找到...'.format(name))
        return []
    # save_json(departments, osp.join(cfg.save_departments_info_root,cfg.VACCINDE_INFO[cfg.customId],
    #                                name + '.json'))
    return departments


# 根据区域id获取该区域的所有的医院信息
def get_all_departments(regionCode='4101'):
    """
    https://wx.scmttec.com/base/department/getDepartments.do?
    offset=0&limit=10&name=&regionCode=&isOpen=1&longitude=&latitude=&sortType=1&vaccineCode=&customId=3&cityName=
    offset=0&limit=10&name=&regionCode=4101&isOpen=1&longitude=&latitude=&sortType=1&vaccineCode=&customId=3
    根据区域id获取该区域的所有的医院信息
    :param regionCode: 请求的区域编号id
    :return: 返回该区域所有的医院信息, [ hospital_1, hospital_2, ..., hospital_(end-offset+1) ]
        {
            code: '0000',
            data: {
                offset: 0                # 当分页时显示的偏移
                end: 4                   # 结束为止的编号，所以当前返回的请求的医院数量就是(end-offset+1)
                total: 13                # 总共的医院数量
                limit: 5                 # 最大可返回的医院数量
                pageNumber: 1            # 当前页码数
                pageListSize: 9          # 每页的数据大小
                pageNumList：[1, 2, 3]   # 页码列表
                rows： [
                    hospital_1, hospital_2, ..., hospital_(end-offset+1)
                ]
            },
            ok: 'true'
        }
        每个医院的信息格式：
            hospital: {
                code: ''            # departmentCode，部门代码
                name: ''            # 名称
                imgUrl: ''          # 图片链接
                regionCode: ''      # 该医院所属地区编号
                address: ''         # 医院地址
                tel:''              # 医院电话
                isOpen: ''          # 是否开放
                latitude:''         # 经度
                longitude: ''       # 纬度
                worktimeDesc: ''    # 工作时间描述
                distance: ''        # 距离
                vaccineCode: ''     # 疫苗编号
                vaccineName: ''     # 疫苗名称
                total: ''           # 总数
                isSeckill: ''       # 是否秒杀
                price: ''           # 价格
                sourceType: ''      #
                isHiddenPrice: ''   #
                depaCodes: ''       # 部门编码
                vaccines: ''        # 疫苗
                depaVaccId: ''      # 部门疫苗id，重要重要重要！！！！请求某一个医院的信息时用到这个字段
                stopSubscribe: ''   # 停止订阅
            }
    """
    params = {'regionCode': regionCode,  # 请求的区域编号
              'customId': cfg.customId,  # 3-九价疫苗；2-四价疫苗；1-二价疫苗
              'limit': 50,  # 请求的医院最大数目
              'isOpen': 1,
              'sortType': 1,
              # 'vaccineCode': 0,             # 疫苗编号
              'offset': 0,
              # 'name': '新郑市龙湖镇卫生院',  # 医院名字
              'longitude': 0,  # 经度
              'latitude': 0,  # 纬度
              }
    res = GET(cfg.URLS['ALL_DEPARTMENTS'], params, headers=cfg.REQ_HEADERS, verify=False)

    total = res['data']['total']
    if params['limit'] < total:
        params['limit'] = total
        print(params)
        res = GET(cfg.URLS['ALL_DEPARTMENTS'], params, headers=cfg.REQ_HEADERS, verify=False)

    departments = res['data']['rows']

    return departments

