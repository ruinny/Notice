import django
import os
import sys

sys.path.append("../")
os.environ.update({"DJANGO_SETTINGS_MODULE": "Notice.settings"})
django.setup()
from sendpack.functions import *
import time

notice_list = get_list()
send_wxpusher(get_dp_simple_notice(30))
for name in notice_list:
    notice = fetch_data(3, name)  # 获取提醒内容
    if notice[3] != 0:
        sendmail(notice[0], notice[2])  # 发送提醒邮件
        sendsms(notice[1], notice[3], 3)  # 发送提醒短信
        print(notice[2] + '有' + str(notice[3]) + '条提醒已经发送成功')
        time.sleep(15)
    else:
        print("Nothing to notice")

if datetime.datetime.today().strftime('%A') == 'Monday':
    for name in notice_list:
        notice = fetch_data(30, name)  # 获取提醒内容
        if notice[3] != 0:
            sendmail(notice[0], notice[2])  # 发送提醒邮件
            sendsms(notice[1], notice[3], 30)  # 发送提醒短信
            print(notice[2] + '有' + str(notice[3]) + '条提醒已经发送成功')
            time.sleep(15)
        else:
            print("Nothing to notice")