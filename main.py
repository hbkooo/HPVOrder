# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests
from YuemiaoPublicAccount.yuemiao import YueMiao
import sys
import argparse

cookie = "Cookie: UM_distinctid=176d61668197b-02a1e977b885ce-67341f2e-448e0-176d616681a15f; " \
         "_xxhm_=%7B%22address%22%3A%22%22%2C%22awardPoints%22%3A0%2C%22birthday%22%3A838915200000%2C%22createTime%22" \
         "%3A1609909609000%2C%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen" \
         "%2FxjC97SLpMq3cvXlkz52xb36XWnHt7oVewePaFv0VDRL6cKEx2b9SIkIzjHQMO6WKsUevtbvpYOPDiakZ0mJ6cXHibWdf7oXEWS%2F132" \
         "%22%2C%22id%22%3A9787092%2C%22idCardNo%22%3A%%22%2C%22isRegisterHistory%22%3A0%2C" \
         "%22latitude%22%3A0.0%2C%22longitude%22%3A0.0%2C%22mobile%22%3A%2215927037762%22%2C%22modifyTime%22" \
         "%3A1610450895000%2C%22name%22%3A%22%E5%88%98%E9%A6%99%E7%8E%89%22%2C%22nickName%22%3A%22%E9%98%B3%E5%85%89" \
         "%E4%B8%8B%E7%9A%84%E9%82%A3%E4%BA%BA%22%2C%22openId%22%3A%22oWzsq537IeWEv_66fdxl2rB6Iau4%22%2C%22regionCode" \
         "%22%3A%22410104%22%2C%22registerTime%22%3A1610450895000%2C%22sex%22%3A2%2C%22source%22%3A1%2C%22uFrom%22%3A" \
         "%22depa_vacc_detail%22%2C%22unionid%22%3A%22oiGJM6N1lDPclKX-5C46AaSitUXw%22%2C%22wxSubscribed%22%3A1%2C" \
         "%22yn%22%3A1%7D; _xzkj_=wxtoken:81ef8042d10ceae7f337f34afc100296_626cbc4a28cad4ad521b6d2ef1d68845; " \
         "MEIQIA_TRACK_ID=1n0u3doGc1unZkM1ex2PVknFjHA; MEIQIA_VISIT_ID=1n0u3j3blqbzmDDRXA0GeWEciqJ; " \
         "CNZZDATA1261985103=1371327906-1609907284-%7C1610545073 "
tk = 'wxtoken:81ef8042d10ceae7f337f34afc100296_3682532d8992f4ca0b6f21175fd4a029'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('op', help='choose [ order | subscribe | save | info ]；'
                                   'order:开始预约；subscribe：开始订阅；'
                                   'save：查找已经到苗的所有社区信息（只针对--province某一个省或者不传参针对全国）；'
                                   'info：查看保存社区信息')
    # 三个优先级从高到低
    parser.add_argument('--region_id', help='地区id（4101河南郑州）')  # , default='4101')     # 4101-郑州区域id
    parser.add_argument('--name', help='社区医院名称（新郑市龙湖镇卫生院）')  # , default='新郑市龙湖镇卫生院')
    parser.add_argument('--province', help='选择省份（河南省）', default='河南省')
    return parser.parse_args()


if __name__ == '__main__':

    yuemiao = YueMiao(tk=tk, cookie=cookie)

    args = parse_args()
    op = args.op
    name = args.name
    province = args.province
    region_id = args.region_id

    if op == 'order':
        # 开始预订
        if region_id is not None:
            flag = yuemiao.find_is_order(regionCode=region_id)
        elif name is not None:
            # departmentName = 新郑洪圣堂医院预防接种门诊
            yuemiao.order_by_name(departmentName=name)
        else:
            flag = yuemiao.find_is_order(province=province)
    elif op == 'subscribe':
        # 开始订阅
        if region_id is not None:
            flag = yuemiao.subscribe_by_region_id(region_id=region_id)
        elif name is not None:
            yuemiao.subscribe_by_name(name=name)
        else:
            flag = yuemiao.subscribe_by_province(province=province)
    elif op == 'save':
        if province is not None and province != "":
            # 保存某个省的所有一到疫苗的社区信息
            print("[info]: 查找{}内的已经到苗信息".format(province))
            yuemiao.query_arrive_vaccine_by_province(province=province)
        else:
            # 保存全国所有一到疫苗的社区信息
            print("[info]: 查找全国范围内的已经到苗信息")
            yuemiao.query_arrive_vaccine_in_china()
    elif op == 'info':
        if region_id is not None:
            yuemiao.get_all_departments_by_code(regionCode=region_id)
        elif name is not None:
            yuemiao.get_all_departments_by_name(name=name)
        elif province is not None:
            yuemiao.get_all_departments_by_province(province=province)

    else:
        print('[error]: 你输入的操作"{}" 不是 "[ order | subscribe | save | info ]"里的一个'
              .format(op))

