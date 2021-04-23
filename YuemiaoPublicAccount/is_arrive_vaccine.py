# encoding: utf-8
import json
import os.path as osp
import YuemiaoPublicAccount.config as cfg
from YuemiaoPublicAccount.all_city_code import save_all_provinces
from YuemiaoPublicAccount.department_info import get_all_department_vaccine_infos, get_department_by_name
from YuemiaoPublicAccount.util import save_json
from YuemiaoPublicAccount.all_city_code import get_province_code

"""
department: {
        "id":4120,
        "departmentCode":"4201110017",
        "vaccineCode":"8803",
        "departmentName":"湖北省疾病预防控制中心门诊部",
        "describtion":"<p><img src=\"https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B7HPV_1593588304636.png\" alt=\"九价HPV.png\"/></p>",
        "instructionsUrls":[],
        "isArriveVaccine":1,
        "name":"九价HPV疫苗（进口）",
        "prompt":"",
        "subscribed":2,
        "total":31,
        "stopSubscribe":0,
        "sourceType":1,
        "urls":["https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B71_1585135836062.jpg",
            "https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B72_1585135836131.jpg",
            "https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B73_1585135836184.jpg",
            "https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B74_1585135836239.jpg"],
        "items":[
            {
                "id":4120,
                "vaccineCode":"8803",
                "factoryName":"默沙东集团",
                "specifications":"0.5mL/支",
                "name":"九价HPV疫苗（进口）",
                "price":0,
                "sourceType":1,
                "isNoticedUserAllowed":1
            }
        ],
        "departmentVaccineId":4120,
        "isNoticedUserAllowed":1
}
"""

"""
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


# 根据传入的所有的社区疫苗信息列表判断是否有已经到苗的社区
def is_arrive_vaccine(departmentVaccineInfos):
    """
    根据传入的所有的社区疫苗信息列表判断是否有已经到苗的社区
    :param departmentVaccineInfos: 社区疫苗的信息的列表
    :return: 有疫苗已经到的社区的信息列表 [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: **， 该疫苗描述: **， 是否可秒杀: ** }
    """
    results = []
    for info in departmentVaccineInfos:
        departmentName = info['departmentName']
        isArriveVaccine = info['isArriveVaccine']
        vaccine_description = info['name']
        if isArriveVaccine == 0:
            continue
        departments = get_department_by_name(departmentName)
        if len(departments) == 0:
            print('社区{}暂时没有找到...'.format(departmentName))
            continue
        department = departments[0]
        address = department['address']
        tel = department['tel']
        isSeckill = department['isSeckill']
        result = {'社区名字': departmentName,
                  '社区电话': tel,
                  '社区地址': address,
                  '该疫苗描述': vaccine_description,
                  '是否可秒杀': isSeckill}
        results.append(result)
    return results


# 保存查询省的所有的社区疫苗信息到Excel表格中
def get_department_vaccine_info_by_province(province):
    """
    根据省的名字获取该省的所有的社区疫苗信息
    :param province:
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
    province_code = get_province_code(province=province)
    departmentVaccineInfos = get_all_department_vaccine_infos(province_code)
    save_json(departmentVaccineInfos, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                               province + '_社区疫苗信息.json'))
    print('[info]: 从"{}"一共查找保存{}社区疫苗信息'.format(province, len(departmentVaccineInfos)))
    return departmentVaccineInfos


# 保存全国的所有社区疫苗信息
def get_china_department_vaccine_info():
    departmentVaccineInfos = get_all_department_vaccine_infos('')
    save_json(departmentVaccineInfos, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                               '全国社区疫苗信息.json'))
    print('[info]: 全国范围内一共查找保存{}社区疫苗信息'.format(len(departmentVaccineInfos)))
    return departmentVaccineInfos


# 查询某省内所有有苗的信息
def query_is_arrive_vaccine_by_province(province):
    """
    查询某省内所有有苗的信息
    :param province: 省的名称：河南省
    :return: 有疫苗已经到的社区的信息列表 [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: **， 该疫苗描述: **， 是否可秒杀: ** }
    """
    departmentVaccineInfos = get_department_vaccine_info_by_province(province=province)
    results = is_arrive_vaccine(departmentVaccineInfos)
    if len(results) != 0:
        save_json(results, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    province + "_社区疫苗已经到苗.json"))
    # print(results)
    print('[info]: 从"{}"查找保存的{}社区疫苗信息中一共有{}社区医院已经到苗\n\n'.format(province, len(departmentVaccineInfos), len(results)))
    return results


# 查找全国范围内的到苗社区
def query_is_arrive_vaccine_in_china():
    """
    查找全国范围内的到苗社区
    :return: 有疫苗已经到的社区的信息列表 [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: **， 该疫苗描述: **， 是否可秒杀: ** }
    """
    departmentVaccineInfos = get_china_department_vaccine_info()
    results = is_arrive_vaccine(departmentVaccineInfos)
    if len(results) != 0:
        save_json(results, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    "全国社区疫苗已经到苗.json"))
    # print(results)
    print('[info]: 全国范围内查找保存{}社区疫苗信息中有{}社区医院已经到苗\n\n'.format(len(departmentVaccineInfos), len(results)))
    return results
