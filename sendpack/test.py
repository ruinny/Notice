import django
import os
import sys
sys.path.append("../")
os.environ.update({"DJANGO_SETTINGS_MODULE": "Notice.settings"})
django.setup()

from sendpack.functions import *

data = webpack.models.Notice.objects.order_by('notice_date').filter(name='孙睿谦',
                                            notice_date__lte=(datetime.datetime.now() + datetime.timedelta(
                                                days=2)).strftime("%Y-%m-%d"),
                                            notice_date__gte=datetime.datetime.now().strftime("%Y-%m-%d"))
for i in data:
    print(str(i.notice_date)+" "+i.context)
#data2=webpack.models.Contact.objects.get(name='孙睿谦').email
#print(data)
#print(fetch_data(30,'孙睿谦'))
print(datetime.datetime.today().strftime('%A'))
