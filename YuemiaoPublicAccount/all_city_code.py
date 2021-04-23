# encoding: utf-8
"""
保存所有的城市地区的编号code
"""
from YuemiaoPublicAccount.util import *
import YuemiaoPublicAccount.config as cfg


def convert(info_list):
    """
    convert list to dict
    :param info_list: [{'name': '郑州市', 'value': '4101'},  ... , {'name': '济源市', 'value': '4190'}]
    :return: dict { '郑州市':4101, ... , '济源市':4190}
    """
    dicts = {}
    for item in info_list:
        dicts[item['name']] = item['value']
    return dicts


def save_all_city_info():
    """
    获取保存所有的城市代码信息
    :return: None
    """
    save_root = cfg.save_city_code_root
    mkdir(save_root)

    if not osp.exists(osp.join(save_root, 'provinces.json')):
        provinces = save_all_provinces()
    else:
        f = open(osp.join(save_root, 'provinces.json'), encoding='utf-8')
        provinces = json.load(f)
        f.close()

    for province in provinces:
        if osp.exists(osp.join(save_root, province+'.json')):
            # 该省的信息已经存在，跳过
            continue
        print('[info] : process {} province'.format(province))
        p_value = provinces[province]

        params = {'parentCode': p_value}
        result = GET(cfg.URLS['INFO'], params, verify=False)  # 发起请求，获取该省的所有城市信息

        result_province = {}

        cities = convert(result['data'])
        for city in cities:
            c_value = cities[city]

            if len(str(c_value)) == 6:
                # 直辖市
                save_json(cities, osp.join(save_root, province + '.json'))
                break

            params = {'parentCode': c_value}
            result = GET(cfg.URLS['INFO'], params, verify=False)  # 发起请求，获取该城市的所有区信息
            area = convert(result['data'])
            value = {'value': c_value, 'area': area}
            # 该城市的区信息
            result_province[city] = value

        if len(result_province) != 0:
            save_json(result_province, osp.join(save_root, province + '.json'))
    print('save all info done.')


# 保存所有的省信息到 provinces.json 文件中
def save_all_provinces():
    """
    返回所有省的编号
    :return:
    {
        "北京市": "11", "天津市": "12", "河北省": "13", "山西省": "14", "内蒙古自治区": "15", "辽宁省": "21",
        "吉林省": "22", "黑龙江省": "23", "上海市": "31", "江苏省": "32", "浙江省": "33", "安徽省": "34",
        "福建省": "35", "江西省": "36", "山东省": "37", "河南省": "41", "湖北省": "42", "湖南省": "43",
        "广东省": "44", "广西壮族自治区": "45", "海南省": "46", "重庆市": "50", "四川省": "51", "贵州省": "52",
        "云南省": "53", "西藏自治区": "54", "陕西省": "61", "甘肃省": "62", "青海省": "63", "宁夏回族自治区": "64",
        "新疆维吾尔自治区": "65", "香港": "81"
    }
    """
    save_root = cfg.save_city_code_root
    mkdir(save_root)

    result = GET(cfg.URLS['INFO'], verify=False)
    if not result or not result['ok']:
        print('[error] : request all provinces failed ...')
        return
    provinces = convert(result['data'])
    save_json(provinces, osp.join(save_root, 'provinces.json'))
    print('[info]: 成功保存所有的省份编号信息到文件 {} 中'.format(osp.join(save_root, 'provinces.json')))
    return provinces


# 通过省份名称查找该省份的code编码
def get_province_code(province):
    """
    通过省份名称查找该省份的code编码
    :param province: 查询的省份
    :return: 返回该省份的编码code
    """
    if not osp.exists(osp.join(cfg.save_city_code_root, 'provinces.json')):
        provinces = save_all_provinces()
    else:
        f = open(osp.join(cfg.save_city_code_root, 'provinces.json'), encoding='utf-8')
        provinces = json.load(f)
        f.close()
    if province not in provinces:
        print('[error]: 你输入的省份"{}"不在已知的所有省份 {} 中'.format(province, provinces.keys()))
        exit()
    return provinces[province]
