from django.shortcuts import render
import json
import requests
import webpack.models
from django.views.decorators.csrf import csrf_exempt



# Create your tests here.
"""
headers = {'Content-Type': 'application/json'}
url='http://wxpusher.zjiecode.com/api/fun/create/qrcode'
data={
    "appToken":"AT_RF9Utbh6MVA9MQDkdEzO5Ap9LOXZZzIo",
    "extra":"15063641818",
    "validTime":1800
}
req = requests.post(url, data=json.dumps(data), headers=headers)
#user=json.loads(req.content.decode(encoding='utf-8'))
print(json.loads(req.content.decode()).get('data').get('url'))
#qr_url=user['data']['url']



data = {
            "appToken": "AT_RF9Utbh6MVA9MQDkdEzO5Ap9LOXZZzIo",
            "content": "get success",
            "contentType": 1,
            "topicIds": [

            ],
            "uids": [
                "UID_skgybRNj4CtHTOMhD2rxLjYSAqJR"
            ],
            # "url":"http://wxpusher.zjiecode.com"
        }
headers = {'Content-Type': 'application/json'}
wxsender = requests.post("http://127.0.0.1:8000/bind_wx_back", data=json.dumps(data), headers=headers)
print(wxsender.content.decode())
"""

user=webpack.models.Contact.objects.get(pk=4)
print(user.name)

