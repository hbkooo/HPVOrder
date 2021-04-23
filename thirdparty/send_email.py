# encoding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import thirdparty.config as cfg


def send_email(content, subject='约苗可预约结果'):
    """
    发送邮件
    :param content: 要发送的消息内容
    :param subject: 邮件主题
    :return:
    """
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("约苗消息提示", 'utf-8')  # 发送者
    message['To'] = Header("约苗消息，可预约", 'utf-8')  # 接收者

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        smtpObj.login(cfg.sender, cfg.passwd)
        smtpObj.sendmail(cfg.sender, cfg.email_receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")


# send_email("test")
