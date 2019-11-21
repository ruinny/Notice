import django
import os
import sys
import requests
import json
sys.path.append("../")
os.environ.update({"DJANGO_SETTINGS_MODULE": "Notice.settings"})
django.setup()

from sendpack.functions import *
from wxsender.views import *

data = webpack.models.Notice.objects.order_by('notice_date').filter(name='孙睿谦',
                                            notice_date__lte=(datetime.datetime.now() + datetime.timedelta(
                                                days=10)).strftime("%Y-%m-%d"),
                                            notice_date__gte=datetime.datetime.now().strftime("%Y-%m-%d"))
sms=""
for i in data:
    sms=sms+str(i.notice_date)+" "+i.context+"\n"
#data2=webpack.models.Contact.objects.get(name='孙睿谦').email
#print(data)
#print(fetch_data(30,'孙睿谦'))
#print(datetime.datetime.today().strftime('%A'))

print(sms)
uid=["UID_skgybRNj4CtHTOMhD2rxLjYSAqJR"]
webpack.models.Contact.objects.filter(name='')
sendwx(sms,uid)

