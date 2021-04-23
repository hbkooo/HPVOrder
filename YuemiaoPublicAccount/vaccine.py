# encoding: utf-8
"""
疫苗信息
"""
from YuemiaoPublicAccount.util import *
import YuemiaoPublicAccount.config as cfg


def get_vaccine_info(depaCode, depaVaccId, vaccineCode=8803):
    """
    在某个部门发起订阅
    :param depaCode: 区域编码
    :param depaVaccId: 部门疫苗id，医院唯一标识
    :param vaccineCode: 疫苗编号, 8803默认是九价疫苗编号，8802是四价，8806是二价国产，8801二价进口
    :return:
    {
        "code":"0000",
        "data": {
            "code":"8803",
            "name":"九价HPV疫苗（进口）",
            "yn":1,
            "intro":"16-26岁女性 预防92%的宫颈癌 90%的生殖器疣",
            "ageStart":16,
            "ageEnd":26,
            "id":11839,
            "price":132000,
            "total":0,
            "subscribed":0,
            "prompt":"预约成功必须按时前往门诊接种，预约疫苗免费，完成接种后请点击确认接种。\n一周之内没有生病吃药，避开例假期。",
            "vaccineProgram":"M0,M2,M6",
            "isArriveVaccine":0,
            "serviceFee":200,
            "isSubscribeAll":0,
            "urls":["https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%252525252525E4%252525252525B9%2525252525259D%252525252525E4%252525252525BB%252525252525B72_1585135836131_1594021631099_1594024001764_1594080370577_1594454847430_1594456397270_1606270667836.jpg","https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%252525252525E4%252525252525B9%2525252525259D%252525252525E4%252525252525BB%252525252525B71_1585135836062_1594021630960_1594024001730_1594080370536_1594454847394_1594456397339_1606270667871.jpg","https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%252525252525E4%252525252525B9%2525252525259D%252525252525E4%252525252525BB%252525252525B73_1585135836184_1594021631153_1594024001797_1594080370623_1594454847468_1594456397404_1606270667897.jpg","https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%252525252525E4%252525252525B9%2525252525259D%252525252525E4%252525252525BB%252525252525B74_1585135836239_1594021631203_1594024001849_1594080370656_1594454847501_1594456397372_1606270667939.jpg"],
            "isSeckill":0,
            "isHiddenPrice":0,
            "instructionsUrls":[],
            "specifications":"0.5mL/支",
            "factoryName":"默沙东集团",
            "productId":128,
            "monthStart":192,
            "monthEnd":324,
            "sexRequired":2,
            "regionRequired":"",
            "pay":false
        },
        "ok":true
    }
    """

    # https://wx.scmttec.com/base/department/vaccine.do?vaccineCode=8802&depaCode=4101840002&departmentVaccineId=10162&isShowDescribtion=false
    params = {
        'depaCode': depaCode,
        'departmentVaccineId': depaVaccId,
        'vaccineCode': vaccineCode,
    }
    response = GET(cfg.URLS['VACCINE_INFO'], params, headers=cfg.REQ_HEADERS, verify=False)
    return response


