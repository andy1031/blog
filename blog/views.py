from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from blog import forms, models
from django.db.models import Count


def login(request):    #AJAX登陆校验
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据ret
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名，密码，验证码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        valid_code = request.POST.get("valid_code")
        # print(valid_code)
        # print(request.session.get("valid_code", ""))
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
            # 验证码正确，利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd) # 校验通过拿到通过的对象user，校验不通过，user为空
            if user:   # 用户名密码正确
                auth.login(request, user)    # 将已登陆的用户信息封装到requst.user中（session的原理）
                # print(request.user.username)
                ret["msg"] = "/index/"    # 将路径添加到返回数据中
            else:    # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"
        return JsonResponse(ret)
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('/index/')


def index(request):
    article_list = models.Article.objects.all()
    print(article_list)
    return render(request, "index.html", {"article_list": article_list})



# 生成随机验证码图片
from PIL import Image,ImageDraw,ImageFont
import random

def get_valid_img(request):
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # 生成一张颜色随机的图片画布
    img_obj=Image.new('RGB',(220,35),get_random_color())
    # 生成图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 生成字体
    font = ImageFont.truetype('static/font/kumo.ttf',30)
    # 生成5位的随机字符
    tmp_list= []
    for i in range(5):
        u = chr(random.randint(65,90))
        l = chr(random.randint(97,122))
        n = str(random.randint(0,9))
        tmp = random.choice([u,l,n])
        tmp_list.append(tmp)
        # 将字符画到画布上
        draw_obj.text((20+20*i,0),tmp,fill=get_random_color(),font=font)

    # # 给验证码加干扰
    # width =220
    # height = 35
    # # 给图片加5条干扰线
    # for i in range(5):
    #     x1 = random.randint(0,width)
    #     x2 = random.randint(0,width)
    #     y1 = random.randint(0,height)
    #     y2 = random.randint(0,height)
    #     # 在画布上画上干扰线
    #     draw_obj.line((x1,x2,y1,y2),fill = get_random_color())
    #
    # # 给图片加40个干扰点
    # for i in range(40):
    #     # 生成干扰点
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     # 在画布上画上干扰线
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # # 将图片保存到本地
    # with open('s10.png','wb')as f:
    #     img_obj.save(f,'png')
    # # 将图片返回给页面
    # with open('s10.png','rb')as f:
    #     data = f.read()

    # 将随机数保存到session中
    request.session['valid_code']=''.join(tmp_list)
    # 生成的图片不需要保存到硬盘，直接保存到缓存就可以
    from io import BytesIO
    io_obj = BytesIO()  # 生成一个缓存区
    img_obj.save(io_obj,'png')  #将图片保存到缓存区
    data = io_obj.getvalue()    # .getvalue 读取缓存区的所有内容
    return HttpResponse(data)


#
# from django.views.decorators.csrf import csrf_exempt
# # 注册的视图函数
# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         print(request.POST)
#         new_name = request.POST.get('name')
#         new_pwd = request.POST.get('pwd')
#         new_email = request.POST.get('emial')
#         # User.objects.create(username = new_name,password=new_pwd)  # 明文密码
#         models.UserInfo.objects.create_user(username = new_name,password=new_pwd,email=new_email)  # 加密密码
#         return redirect('/login/')
#     return render(request, "register.html")


def register(request):
    if request.method == 'POST':
        ret={'status':0,'msg':''}
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('re_password')
            avatar_img = request.FILES.get('avatar')             # 上传的文件从request.FILES中取
            models.UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar_img)
            ret['msg']='/index/'
            return JsonResponse(ret)
        else:
            ret['status']=1
            ret['msg']=form_obj.errors
            return JsonResponse(ret)
    form_obj = forms.RegForm()
    return render(request,'register.html',{'form_obj': form_obj})

def check_name(request):
    ret={'status':0,'msg':''}
    username = request.GET.get('username')
    if models.UserInfo.objects.filter(username=username):
        ret['status']=1
        ret['msg']='用户名已被注册'
        return JsonResponse(ret)


def home(request,username):   # url接受用户名
    # 从userinfo表取出用户
    user = models.UserInfo.objects.filter(username=username)[0]
    if not user:
        return HttpResponse(404)
    else:
        article_list = models.Article.objects.filter(user=user)
        blog = user.blog  # 根据uer找到blog

        return render(request,'home.html',{
            'username':username,
            'blog':blog,
            'article_list':article_list,

        })

def article_detail(request,username,pk):  # 接收两个参数
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    article_obj = models.Article.objects.filter(pk=pk).first()
    # 取到当前文章的所有评论
    comment_list = models.Comment.objects.filter(article_id=pk)

    return render(request,'article_detail.html',{'username':username,'article_obj':article_obj,'blog':blog,'comment_list':comment_list})

# 文章点赞
import json
from django.db.models import F
def up_down(request):
    ret = {'status': 0}
    # 从请求数据中取值，取数据库生成数据
    is_up = json.loads(request.GET.get('is_up'))   # 前端传过来的时字符串，需要转换城布尔值
    article_id = request.GET.get('article_id')
    user = request.user   # 取出当前登陆用户
    try:   #未点击过
        # 生成点赞数据
        models.ArticleUpDown.objects.create(user=user,article_id=article_id,is_up=is_up)
        # 更新文章点赞表(up_count+1)
        models.Article.objects.filter(pk=article_id).update(up_count=F('up_count')+1)
    except Exception as e:  # 报错，说明已点击过
        ret['status'] = 1
        # 取到之前点击的数据，传给前端
        ret['first_seclet'] = models.ArticleUpDown.objects.get(user=user,article_id=article_id,).is_up
    return JsonResponse(ret)

# 文章评论
def comment(request):
    print(request.POST)
    ret ={}
    # 从请求数据中取值，取数据库生成数据
    article_id=request.POST.get('article_id')
    user=request.user
    content=request.POST.get('content')
    pid=request.POST.get('pid')
    if not pid:  # pid为空，则为根评论
        comment_obj= models.Comment.objects.create(article_id=article_id,user=user,content=content)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, user=user, content=content,parent_comment_id=pid)
    # 更新文章表的评论数据
    models.Article.objects.filter(pk=article_id).update(comment_count=F('comment_count')+1)
    ret['create_time']=comment_obj.create_time
    ret['content']=comment_obj.content
    ret['username']=comment_obj.user.username
    print(ret)
    return JsonResponse(ret)

# 获取评论树
def comment_tree(request,article_id):
    # 获取 该文章的 评论信息
    ret = list(models.Comment.objects.filter(article_id=article_id).values('pk','content','parent_comment_id'))
    return JsonResponse(ret,safe=False)

# 写博客
def add_article(request):
    if request.method == 'POST':
        print(request.POST)
        article_title=request.POST.get('title')
        article_content=request.POST.get('article_content')
        user =request.user

        # =========使用BeautifulSoup对文字进行处理=========
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content,'html.parser')  # 用BeautifulSoup解析html格式
        desc = bs.text[0:150]+'...'      # 取出字符中的文字，切片前150
        # 过滤非法标签
        for tag in bs.find_all():   # 遍历所有标签
            if tag.name == 'script':   # 找到script标签
                tag.decompose()   #删除script标签

        article_obj=models.Article.objects.create(user=user,title=article_title,desc=desc)
        models.ArticleDetail.objects.create(content=str(bs),article=article_obj)
    return render(request,'add_article.html')

# 文件上传
from myblog import settings
import os

def upload(request):
    # print(request.FILES)
    # print(request.FILES.get('imgFile'))
    # print(request.FILES.get('imgFile').name)

    file_obj = request.FILES.get('imgFile')
    path = os.path.join(settings.MEDIA_ROOT,'article_img',file_obj.name) # 设置上传文件的保存路径
    with open(path,'wb')as f:
        for i in file_obj:
            f.write(i)

    ret={
        'error': 0,   # 表示未出错
        'url': '/media/article_img/'+file_obj.name,  # 图片预览链接
    }

    return HttpResponse(json.dumps(ret))   # 前端只能接受json格式

