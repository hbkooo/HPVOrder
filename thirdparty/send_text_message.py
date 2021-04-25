# encoding: utf-8
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import thirdparty.config as cfg


class ZhenziSmsClient(object):
    def __init__(self, apiUrl, appId, appSecret):
        self.apiUrl = apiUrl
        self.appId = appId
        self.appSecret = appSecret

    def send(self, params):
        data = params
        data['appId'] = self.appId
        data['appSecret'] = self.appSecret
        if 'templateParams' in data:
            data['templateParams'] = json.dumps(data['templateParams'])
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.post(self.apiUrl + '/sms/v2/send.do', data=data, verify=False)
        result = str(response.content, 'utf-8')
        return result

    def balance(self):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret
        }
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning);
        response = requests.post(self.apiUrl + '/account/balance.do', data=data, verify=False);
        result = str(response.content, 'utf-8');
        return result;

    def findSmsByMessageId(self, messageId):
        data = {
            'appId': self.appId,
            'appSecret': self.appSecret,
            'messageId': messageId
        }
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning);
        response = requests.post(self.apiUrl + '/smslog/findSmsByMessageId.do', data=data, verify=False);
        result = str(response.content, 'utf-8');
        return result;


# 发送短信提醒
def send_text_message(result):
    """
    发送短信提醒
    :param result: 传入一个包含两个元素的列表集合： [ param1 param2 ]， 例：['9988', '15分钟']
    :return: {"code":108,"data":"余额不足"}
    """
    params = {'number': cfg.receiver_tel,
              'templateId': cfg.zhenzi_templateId,
              'templateParams': result}
    data = params
    data['appId'] = cfg.zhenzi_AppId
    data['appSecret'] = cfg.zhenzi_AppSecre
    if 'templateParams' in data:
        data['templateParams'] = json.dumps(data['templateParams'])
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response = requests.post(cfg.zhenzi_url + '/sms/v2/send.do', data=data, verify=False)
    result = str(response.content, 'utf-8')
    print(result)
    return result


def test():
    url = 'https://sms_developer.zhenzikj.com'
    AppId = 123456
    AppSecre = '12345678-1234-1234-1234-123456789123'

    params = {}
    params['number'] = '15927037762'
    params['templateId'] = '3338'
    params['templateParams'] = ['9988', '15分钟']
    client = ZhenziSmsClient(url, AppId, AppSecre)
    print(client.send(params))


# test()
# send_text_message(['海沧区新阳街道社区卫生服', '5分钟'])
