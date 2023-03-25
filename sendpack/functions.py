# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import requests
import webpack.models
import os


def get_list():
    list_query_list = webpack.models.Contact.objects.all()
    lists = []
    for query in list_query_list:
        lists.append(query.name)
    return lists


def fetch_data(days, name):
    mail_insert = ""
    data = webpack.models.Notice.objects.order_by('notice_date').filter(name=name,
                                                notice_date__lte=(datetime.datetime.now() + datetime.timedelta(
                                                    days=days)).strftime("%Y-%m-%d"),
                                                notice_date__gte=datetime.datetime.now().strftime("%Y-%m-%d"))
    for query in data:
        mail_insert = mail_insert + "<tr>" + "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" \
                   % (query.name, query.context, query.notice_date, query.cc_from) + "</tr>"

    tel = webpack.models.Contact.objects.get(name=name).tel
    email = webpack.models.Contact.objects.get(name=name).email
    wxuid = webpack.models.Contact.objects.get(name=name).wxuid
    file = open('mail.html','r',encoding='UTF-8')
    content = file.read()
    pos=content.find('<!--table postion-->')
    if pos != -1:
        content=content[:pos] + mail_insert + content[pos:]
        #file=open('mail.html','w',encoding='UTF-8')
        #file.write(content)
        #file.close()
    return content, tel, email, len(data), wxuid


def sendmail(msg_content, receiver):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "notice-mee@qq.com"  # 用户名
    mail_pass = "zscfpxsnbkhydifc"  # 口令
    sender = 'notice-mee@qq.com'
    receivers = ['notice-mee@qq.com']
   
    receivers.append(receiver)
    message = MIMEText(msg_content, 'html', 'utf-8')
    # message['From'] = Header("notice-mee@qq.com", 'utf-8')
    message['From'] = 'Notice-mee'
    # message['To'] =  Header("15063641818@139.com", 'utf-8')
    message['To'] = ";".join(receivers)
    subject = '重要工作提醒  - ' + datetime.datetime.now().strftime("%Y-%m-%d")
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        #print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return


def sendsms(number, count, days):
    # 短信应用 SDK AppID
    appid = 1400218669  # SDK AppID 以1400开头
    # 短信应用 SDK AppKey
    appkey = "ec3e0916afd945d1ab8c1f610b186387"
    # 需要发送短信的手机号码
    phone_numbers = []
    phone_numbers.append(number)
    # 短信模板ID，需要在短信控制台中申请
    template_id = 375144  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
    # 签名
    sms_sign = "Anynicom"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请

    ssender = SmsSingleSender(appid, appkey)
    params = []
    params.append(days)  # 当模板没有参数时，`params = []`
    params.append(count)
    try:
        result = ssender.send_with_param(86, phone_numbers[0], template_id, params, sign=sms_sign, extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    #print(result)


def get_dp_simple_notice(days):
    mail_msg = "%s日内到期事项提醒如下：</br>" % (days)
    data = webpack.models.Notice.objects.order_by('notice_date').filter(notice_date__lte=(datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"),
                                                notice_date__gte=datetime.datetime.now().strftime("%Y-%m-%d"))
    num = 1
    for query in data:
        mail_msg = mail_msg + "%s、%s(%s)</br>" % (num, query.context, query.name)
        num = num + 1
    mail_msg = mail_msg[:-1] + "以上共%s条" % (len(data))
    return mail_msg


def send_wxpusher(content="没有提醒内容"):
    url = "http://wxmsg.dingliqc.com/send?title=到期事项提醒&msg=" + content + "&userIds=orPQ803l5nr5hoUo4x6GwnjYn3ZA9m9BZs7J7q"
    r = requests.get(url)
