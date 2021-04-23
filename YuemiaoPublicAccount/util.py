# encoding: utf-8
"""
一些工具方法操作
"""
import os
import os.path as osp
import json
import requests
import xlwt
import YuemiaoPublicAccount.config as cfg
from thirdparty.send_email import send_email

requests.packages.urllib3.disable_warnings()


def mkdir(path):
    """
    新建文件夹
    :param path: 新建文件夹路径
    :return:
    """
    if not osp.exists(path):
        os.makedirs(path)


mkdir(cfg.save_departments_info_root)
mkdir(cfg.save_city_code_root)


def save_excel(json_list_data, save_path, encoding='utf-8'):
    """
    将 json 数据保存到 Excel 文件中
    :param json_list_data: json的集合数据： [ {}, {} ... {} ]
    :param save_path: 保存路径
    :param encoding: 编码格式
    :return: None
    """
    mkdir(osp.dirname(save_path))
    if not save_path.endswith('xls'):
        save_path += '.xls'

    if len(json_list_data) == 0:
        return
    # print(json_list_data)
    book = xlwt.Workbook(encoding=encoding)
    sheet = book.add_sheet(sheetname='data')

    alignment = xlwt.Alignment()  # Create Alignment
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style = xlwt.XFStyle()  # Create Style
    style.alignment = alignment  # Add Alignment to Style

    keys = list(json_list_data[0].keys())

    for i in range(len(keys)):
        sheet.col(i).width = 3333
        sheet.write(0, i, keys[i], style)

    for row in range(len(json_list_data)):
        item = json_list_data[row]
        # row_ = sheet.col(row)
        # row_.height = 50
        for col in range(len(keys)):
            key = keys[col]
            value = item.get(key, '')
            sheet.write(row + 1, col, value, style)
    book.save(save_path)


def save_json(json_data, save_path, encoding='utf-8', ensure_ascii=False):
    """
    把数据保存到json文件中
    :param json_data: 保存的数据
    :param save_path: 保存的路径
    :param encoding: 保存文件的编码格式，默认为 utf-8
    :param ensure_ascii: 保存json文件时是否确保使用 ascii 编码，默认为False
    :return: None
    """
    mkdir(osp.dirname(save_path))
    with open(save_path, 'w', encoding=encoding) as fw:
        json.dump(json_data, fw, ensure_ascii=ensure_ascii)


def GET(url, params=None, error_exit=False, **kwargs):
    """
    GET请求. 请求返回错误码(4XX,5XX)时退出
    :param url: 请求路径
    :param params: 请求参数
    :param error_exit:返回4XX 5XX错误时 是否退出
    :param kwargs: 附加信息
    :return: 结果JSON
    { code: '0000', data: {}, ok: true/false }
    """
    try:
        response = requests.get(url, params, **kwargs)
        response.raise_for_status()
    except Exception as err:
        error_response = f'URL:{url} ERROR:{err}'
        print('[error] in GET request : ', error_response)
        if error_exit:
            send_email('程序已经退出：GET请求错误，' + error_response, subject="抢苗请求出错")
            exit(1)
        send_email('GET请求错误，' + error_response, subject="抢苗请求出错")
        return None
    else:
        res_json = response.json()
        _suc_msg = f'{url}\n{"-" * 5 + "Request" + "-" * 5}\n{params}\n{"-" * 5 + "Response" + "-" * 5}\n{res_json}\nuseTime:{response.elapsed.total_seconds()}S\n'
        '''
        日志默认级别[WARNING] 考虑最大限度不影响秒杀效果此处以[INFO]记录正常响应的请求(正常响应不代表秒杀成功)\
        即trace.log均不会记录正常响应日志\
        若希望记录响应日志 使用--log指定日志级别
        '''
        # msg=用户登录超时,请重新登入!
        if 'msg' in res_json:
            msg = res_json['msg']
            if '用户登录超时,请重新登入' in msg:
                send_email('约苗提示错误消息：' + str(msg), subject="约苗登录超时")
                print(msg + '\n结束抢苗')
                exit(1)
        # print(_suc_msg)
        # logging.info(_suc_msg)
        return res_json


def POST(url, params=None, error_exit=True, **kwargs):
    """
    POST请求. 请求返回错误码(4XX,5XX)时退出
    :param url: 请求路径
    :param params: 请求参数
    :param error_exit: 返回4XX 5XX错误时 是否退出
    :param kwargs: 附加信息
    :return: 结果JSON
    """
    try:
        response = requests.post(url, data=params, **kwargs)
        response.raise_for_status()
    except Exception as err:
        error_response = f'URL:{url} ERROR:{err}'
        print('[error] : ', error_response)
        # logging.error(error_response)
        if error_exit:
            exit(1)
    else:
        res_json = response.json()
        if 'msg' in res_json:
            msg = res_json['msg']
            if '用户登录超时,请重新登入' in msg:
                send_email('约苗提示错误消息：' + str(msg), subject="约苗登录超时")
                print(msg + '\n结束抢苗')
                exit(1)
        return res_json


def get_server_time():
    """
    获取服务器当前时间
    秒杀开始时间由服务器控制
    :return: 服务器时间
    {"code":"0000","data":"2021-01-14 16:37:10","ok":true}
    """
    # https://wx.scmttec.com/base//time/now.do
    res_json = GET(cfg.URLS['TIME_NOW'], headers=cfg.REQ_HEADERS, verify=False)  # TIME_NOW SERVER_TIME
    if not res_json['ok']:
        print('[error]: 获取服务器时间有误：{}'.format(res_json['msg']))
        exit()
    # print(res_json)
    return res_json['data']


def get_server_time_miaomiao():
    # https://miaomiao.scmttec.com/seckill/seckill/now2.do
    """
    获取服务器的时间戳
    :return: 服务器当前时间戳
    {"code":"0000","data":1610613367514,"ok":true,"notOk":false}
    """
    res_json = POST(cfg.URLS['SERVER_TIME'], verify=False)
    if not res_json['ok']:
        print('[error]: 获取服务器时间有误：{}'.format(res_json['msg']))
        exit()
    return str(res_json['data'])
