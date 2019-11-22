from django.shortcuts import render
import json
import requests
import webpack.models
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def bindwx(request):
    if 'user' in request.session:
        loguser=webpack.models.Contact.objects.filter(pk=request.session['user'])

        return render(request, 'bindwx.html', {'loguser':loguser,'qr':get_qr(request.session['user'])})
    else:
        return render(request,'login.html')

@csrf_exempt
def bind_wx_back(request):
    if request.method == 'POST':
        uid=json.loads(request.body.decode()).get('data').get('uid')
        extra=json.loads(request.body.decode()).get('data').get('extra')
        user = webpack.models.Contact.objects.get(id=extra)
        webpack.models.Contact.objects.filter(id=extra).update(wxuid=uid)
        sms = "您已经成功关注NoticeMe提醒小工具，每天的提醒将会通过这个公众号推送！\n您的绑定账户是："\
              +user.name+"/"+user.email+"/"+user.tel
        sendwx(sms, uid)
    return render(request, 'bindwx.html')


def get_qr(user_id):
    headers = {'Content-Type': 'application/json'}
    url='http://wxpusher.zjiecode.com/api/fun/create/qrcode'
    data={
    "appToken":"AT_RF9Utbh6MVA9MQDkdEzO5Ap9LOXZZzIo",
    "extra":user_id,
    "validTime":1800
    }
    req = requests.post(url, data=json.dumps(data), headers=headers)
    qr_url = json.loads(req.content.decode(encoding='utf-8')).get('data').get('url')
    return qr_url


def sendwx(sms,uid):
    data = {
        "appToken": "AT_RF9Utbh6MVA9MQDkdEzO5Ap9LOXZZzIo",
        "content": sms,
        "contentType": 2,
        "topicIds": [

        ],
        "uids": [
            uid
        ],
        # "url":"http://wxpusher.zjiecode.com"
    }
    headers = {'Content-Type': 'application/json'}
    wxsender = requests.post("http://wxpusher.zjiecode.com/api/send/message", data=json.dumps(data),
                             headers=headers)
    return wxsender
