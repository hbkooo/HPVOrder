# encoding: utf-8
import xlwt
import json
import os.path as osp
import YuemiaoPublicAccount.config as cfg
from YuemiaoPublicAccount.all_city_code import save_all_provinces
from YuemiaoPublicAccount.department_info import get_all_departments
from YuemiaoPublicAccount.util import save_json
from YuemiaoPublicAccount.all_city_code import get_province_code

"""
department: {
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
    isSeckill: 0        # 是否秒杀
    price: ''           # 价格
    sourceType: ''      #
    isHiddenPrice: ''   #
    depaCodes: ''       # 部门编码
    vaccines: ''        # 疫苗
    depaVaccId: ''      # 部门疫苗id，重要重要重要！！！！请求某一个医院的信息时用到这个字段
    stopSubscribe: ''   # 停止订阅
}
"""

"""
    {
        "code":"4201110017",
        "name":"湖北省疾病预防控制中心门诊部",
        "imgUrl":"https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E6%B9%96%E5%8C%97%E7%9C%81%E7%96%BE%E7%97%85%E9%A2%84%E9%98%B2%E6%8E%A7%E5%88%B6%E4%B8%AD%E5%BF%83%E9%97%A8%E8%AF%8A%E9%83%A8%E5%AE%A3%E4%BC%A0%E5%9B%BE_1591338913414.png",
        "regionCode":"420111",
        "address":"武汉市洪山区卓刀泉北路6号",
        "tel":"",
        "isOpen":1,
        "latitude":30.52346,
        "longitude":114.37291,
        "worktimeDesc":"有下列情况之一的，暂缓接种：1.曾感染过新型冠状病毒。2.近一个月内与新型新型冠状病毒感染者、疑似病例有接触者。3.接触家庭成员中近14天内有发热症状者。4.接种当天有发热等不适症状者。\r\n\r\n",
        "distance":4276.9263,
        "vaccineCode":"8803",
        "vaccineName":"九价HPV疫苗（进口）",
        "total":29,
        "isSeckill":0,
        "price":0,
        "sourceType":1,
        "isHiddenPrice":0,
        "depaCodes":[],
        "vaccines":[],
        "depaVaccId":4120,
        "stopSubscribe":0
    }
"""


def is_seckill(departments):
    """
    根据传入的社区信息判断是否有没有可秒杀的社区
    :param departments: 社区集合 [ ]
    :return: 可以秒杀的社区的信息集合 ： [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: ** }
    """
    results = []
    for department in departments:
        department_name = department['name']
        address = department['address']
        tel = department['tel']
        isSeckill = department['isSeckill']
        if isSeckill == 0:
            continue
        result = {'社区名字': department_name,
                  '社区电话': tel,
                  '社区地址': address}
        results.append(result)
    return results


# 查询省的所有的社区医院信息
def get_departments_info_by_province(province):
    """
    查询省的所有的社区医院信息
    :param province: 省份名称：河南省
    :return: 返回该区域所有的医院信息, [ department_1, department_2, ..., department... ]
    department: {
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
    province_code = get_province_code(province=province)
    departments = get_all_departments(province_code)
    save_json(departments, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    province + '_社区信息.json'))
    print('[info]: 从"{}"一共查找保存{}社区医院信息'.format(province, len(departments)))
    return departments


# 保存全国的所有社区医院信息
def get_china_departments_info():
    departments = get_all_departments('')
    save_json(departments, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    '全国社区信息.json'))
    print('[info]: 全国范围内一共查找保存{}社区医院信息'.format(len(departments)))
    return departments


# 查询某省内所有有苗的信息
def query_is_seckill_by_province(province):
    """
    查询某省内所有可秒杀信息
    :param province: 省的名称：河南省
    :return: 可以秒杀的社区的信息集合 ： [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: ** }
    """
    departments = get_departments_info_by_province(province=province)
    results = is_seckill(departments)
    if len(results) != 0:
        save_json(results, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    province + "_社区医院可秒杀苗.json"))
    # print(results)
    print('[info]: 从"{}"查找的{}社区医院中一共有{}可以秒杀\n\n'.format(province, len(departments), len(results)))
    return results


# 查找全国范围内的到苗社区
def query_is_seckill_in_china():
    """
    查找全国范围内的可秒杀疫苗
    :return: 可以秒杀的社区的信息集合 ： [ item1, item2, ... ]
        item : { 社区名字: **， 社区电话: **， 社区地址: ** }
    """
    departments = get_china_departments_info()
    results = is_seckill(departments)
    if len(results) != 0:
        save_json(results, osp.join(cfg.save_departments_info_root, cfg.VACCINDE_INFO[cfg.customId],
                                    "全国社区医院可秒杀.json"))
    # print(results)
    print('[info]: 全国范围内查找的{}社区医院信息中有{}社区可以秒杀\n\n'.format(len(departments), len(results)))
    return results
