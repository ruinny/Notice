from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .form import *
from django.utils import timezone
from django.contrib import messages
import random
from geetest import GeetestLib  # 极验验证
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


# Create your views here.


def index(request):
    contact = Contact.objects.filter(depart='HR')
    if request.method == 'POST':
        form = AddNotice()
        # form = AddNotice(request.POST)
        # if form.is_valid():
        Notice.objects.create(
            name=request.POST['name'],
            context=request.POST['context'],
            notice_date=request.POST['notice_date'],
            contact_id=Contact.objects.get(name=request.POST['name']).id
        )
        check_box_list = request.POST.getlist('cc')
        for checkbox in check_box_list:
            Notice.objects.create(
                name=checkbox,
                cc_from='抄送自' + request.POST['name'],
                context=request.POST['context'],
                notice_date=request.POST['notice_date'],
                contact_id=Contact.objects.get(name=checkbox).id
            )
        messages.success(request, '添加成功')
    else:
        form = AddNotice()
    return render(request, 'index.html', {'form': form, 'contact': contact})


def show(request):
    context = Notice.objects.order_by('notice_date').filter(notice_date__gte=timezone.now(),
                                                            contact_id=request.session.get("user"))

    if "user" in request.session:
        # context = Notice.objects.filter(notice_date__gte=timezone.now())
        if request.GET:
            if request.method == 'GET':
                Notice.objects.filter(pk=request.GET["id"]).delete()
                messages.success(request, '删除成功')
        return render(request, 'show.html', {'context': context})
    else:
        return HttpResponseRedirect("/login")


def showall(request):
    context = Notice.objects.order_by('notice_date').filter(notice_date__gte=timezone.now())
    # context = Notice.objects.filter(notice_date__gte=timezone.now())
    if request.GET:
        if request.method == 'GET':
            Notice.objects.filter(pk=request.GET["id"]).delete()
            messages.success(request, '删除成功')
            return render(request, 'show.html', {'context': context})


def signup(request):
    if request.POST:
        if request.method == 'POST':
            # form = AddNotice(request.POST)
            # if form.is_valid():
            Contact.objects.create(
                name=request.POST['name'],
                tel=request.POST['tel'],
                email=request.POST['mail'],
                depart=request.POST['depart']
            )
            messages.success(request, '添加成功')
    return render(request, 'singup.html')


def dep_index(request):
    contact = Contact.objects.filter(depart=request.path[5:])
    if request.method == 'POST':
        form = AddNotice()
        # form = AddNotice(request.POST)
        # if form.is_valid():
        Notice.objects.create(
            name=request.POST['name'],
            context=request.POST['context'],
            notice_date=request.POST['notice_date'],
            contact_id=Contact.objects.get(name=request.POST['name']).id
        )
        check_box_list = request.POST.getlist('cc')
        for checkbox in check_box_list:
            Notice.objects.create(
                name=checkbox,
                cc_from='抄送自' + request.POST['name'],
                context=request.POST['context'],
                notice_date=request.POST['notice_date'],
                contact_id=Contact.objects.get(name=checkbox).id
            )
        messages.success(request, '添加成功')
    else:
        form = AddNotice()
    return render(request, 'index-2.html', {'contact': contact, 'form': form})


def lists(request):
    return render(request,'lists.html')


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


# 极验验证的id和key
pc_geetest_id = "e8cfb8c01b27e168b7f73e362310d6bd"  # id
pc_geetest_key = "6bbd767dfa467d9280f293865c8c84eb"  # key


def send_message(request):
    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.POST.get('mobile')
    # 通过手机去查找用户是否已经注册
    user = Contact.objects.filter(tel=mobile)
    if len(user) > 2:
        return JsonResponse({'msg': "该手机未注册"})
    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    sendsms(mobile, message_code)
    request.session['message_code'] = message_code
    return JsonResponse({'msg': "发送成功"})


def LoginView(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        """处理登录操作"""
        # 获取post请求参数
        # 获取手机号/短信验证码
        uphone = request.POST.get('mobile')
        code = request.POST.get('code')
        # 检验合法性
        if not all([uphone, code]):
            return render(request, 'login.html', {'errmsg': "手机号和短信验证码不能为空"})
        # 业务处理：短信验证码是否正确
        if request.session.get("message_code") != code:
            return render(request, 'login.html', {'errmsg': "验证码错误"})

        # try:
        #     user = User.objects.create_user(uphone, "qq123@qq.com", code, uphone=uphone)  # type: User
        #     user.save()
        # except IntegrityError:
        #     # 判断用户是否存在
        #     return render(request, 'demo.html', {'errmsg': "用户名已存在"})

        # 这是校验用户名和密码的方法，不适用手机校验
        # user = authenticate(uphone=uphone)

        # 根据手机号查找用户
        user = Contact.objects.filter(tel=uphone)

        # 判断是否未查找到
        if user[0] is None:
            # 判断用户名和密码是否正确
            return render(request, 'login.html', {'errmsg': "尚未注册"})

        # 登录成功后,要跳转到next指向的页面
        # return render(request, 'login.html', {'errmsg': "登录成功"})
        request.session['user'] = Contact.objects.filter(tel=uphone)[0].id
        return HttpResponseRedirect("/show")


def pcgetcaptcha(request):
    """极验验证函数"""
    # 校验参数
    user_id = 'test'
    # 创建GeetestLib对象，极验验证码id/key
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    # 验证初始化预处理.换取status,值为0或1
    status = gt.pre_process(user_id)
    # status  user_id存进session中，用于校验
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    # 验证初始化预处理的时候返回的响应的字典转换成的json字符串
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def sendsms(mobile, passwd):
    # 短信应用 SDK AppID
    appid = 1400218669  # SDK AppID 以1400开头
    # 短信应用 SDK AppKey
    appkey = "ec3e0916afd945d1ab8c1f610b186387"
    # 需要发送短信的手机号码
    phone_numbers = []
    phone_numbers.append(mobile)
    # 短信模板ID，需要在短信控制台中申请
    template_id = 375743  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
    # 签名
    sms_sign = "Anynicom"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请

    ssender = SmsSingleSender(appid, appkey)
    params = []
    params.append(passwd)  # 当模板没有参数时，`params = []`
    try:
        result = ssender.send_with_param(86, phone_numbers[0], template_id, params, sign=sms_sign, extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)


def bad_request(request):
    return render(request, '404.html')


def permission_denied(request):
    return render(request, '404.html')


def page_not_found(request):
    return render(request, '404.html')


def error(request):
    return render(request, '404.html')
