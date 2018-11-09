# -*- coding: utf-8 -*-

from myblog import myglobal
from django.template import Context
from django.shortcuts import render_to_response
from book.models import Article,Answer,Poll,Friendship,auth_profile
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from operator import itemgetter, attrgetter
from book.views import *
# Create your views here.





def alogin(request):
    errors = []
    account = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if account is not None and password is not None:
            user = authenticate(username=account, password=password)
            if user is not None:
                if user.is_active:
                    request.session['username'] = account
                    login(request, user)
                    return render_to_response('登录成功_跳转.html')
                else:
                    errors.append('disabled account')
            else:
                errors.append('invaild user')
    return render_to_response('login.html', {'errors': errors})


def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    email = None
    CompareFlag = False

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2 = request.POST.get('password2')
        if not request.POST.get('email'):
            errors.append('Please Enter email')
        else:
            email = request.POST.get('email')

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('password2 is diff password ')

        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag:
            user = User.objects.create_user(account, email, password)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('login')

    return render_to_response('register.html', {'errors': errors})


def alogout(request):
    del request.session["username"]
    logout(request)
    return HttpResponseRedirect('view_all')











def post(request):
    un = request.session['username']
    if request.GET:
        l = request.GET
        ADD = Article(title=l['tit'],
                            author=un,
                            content=l['con'],
                            user=request.user)
        ADD.save()
        return render_to_response('choose.html',{'right':True})
    else:
        return render_to_response('post1.html',{'right':True,'username':un})


def bg(request):
    return render_to_response('bground.html')


def hot(request):
    username = request.session['username']
    a=Article.objects.order_by("answer_number")
    return render_to_response('hot.html', {'all_article':a,'username':username})
    
    
def view_all(request):                          #为了区别于点链接进入页面和在页面内搜索,用get判断
    print("进入了view_all页面")
    if request.GET:#如果GET字典里面有参数
        error = []
        print("搜索请求")
        keyword = request.GET["keyword"]
        if not keyword:
            print("为空")
            error.append('1')
            print(keyword)
            all_objects = Article.objects.all()
            username = request.session['username']
            attentioned_author = Friendship.objects.filter(from_friend=request.user)
            return render_to_response('view_all.html',
                                      {'error': error, 'all_objects': all_objects, 'username': username,
                                       'attentioned_author': attentioned_author, 'request.user': request.user})
        else:
            print("不为空")
            all_objects = Article.objects.filter(title__icontains=keyword)
            username = request.session['username']
            attentioned_author = Friendship.objects.filter(from_friend=request.user)
            return render_to_response('search_result.html', {'all_objects': all_objects, 'username': username,
                                                                  'attentioned_author': attentioned_author,
                                                                  'request.user': request.user})
    else:
        all_objects = Article.objects.all()
        username = request.session['username']
        attentioned_author = Friendship.objects.filter(from_friend=request.user)
        return render_to_response('view_all.html',{'all_objects':all_objects,'username':username,'attentioned_author': attentioned_author,'request.user':request.user})


def article(request):
    id1 = request.GET["id"]
    one = Article.objects.get(id=id1)
    all_answer = Answer.objects.filter(article_id=one)
    poll_num = one.poll_number
    exist = Poll.objects.filter(article=id1,user=request.user)
    if exist:
        has_polled = True
    else:
        has_polled = False
    return render_to_response('article.html',{'article':one,'all_answer':all_answer,'poll_num':poll_num,'has_polled':has_polled})


def get_poll_article(request):
    id1 = request.GET["id"]
    one = Article.objects.get(id=id1)
    all_answer = Answer.objects.filter(article_id=one)

    add_user = request.user
    add_art = one
    add_poll = Poll(user = add_user,
                    article = add_art,)
    add_poll.save()
    one.poll_number += 1
    one.save()
    has_polled = True
    return render_to_response('article.html', {'article': one, 'all_answer': all_answer, 'poll_num': one.poll_number,'has_polled':has_polled})


def delete_poll_article(request):
    id1 = request.GET["id"]
    one = Article.objects.get(id=id1)
    all_answer = Answer.objects.filter(article_id=one)
    exist = Poll.objects.filter(article=id1, user=request.user)
    exist.delete()
    one.poll_number -= 1
    one.save()
    has_polled = False
    return render_to_response('article.html', {'article': one, 'all_answer': all_answer, 'poll_num': one.poll_number,'has_polled':has_polled})


def answer(request):
    global myglobal
    un = request.session['username']
    if request.method =='GET':
        myglobal.id1 = request.GET["id"]
        myglobal.art = Article.objects.get(id=myglobal.id1)
        return render_to_response('answer.html', {'right': True,'username': un})
    else:
        if request.method == 'POST':
            myglobal.flag2 = True
            add_answer = Answer(author=un,
                 content=request.POST['con'],
                 article_id=myglobal.art,
                 img=request.FILES.get('img')
                            )
            add_answer.save()
            art=Article.objects.get(id=myglobal.id1)
            art.answer_number+=1
            art.save()
        return render_to_response('success.html', {'right': True, 'username': un,'id':myglobal.id1})


def new_msg(request):           #flag1用来控制两条分支  flag1为False表示第二次打开“新消息”，此时把new_answer字段设为False
    global myglobal
    if myglobal.flag2:
        myglobal.flag2 = False
        user = request.user
        all_art = Article.objects.filter(user=user)
        new = []
        for a in all_art:
            all_answer = Answer.objects.filter(article_id=a)
            new.extend(list(all_answer.filter(new_answer=True)))#filter不可以append
        return render_to_response('new_msg.html',{'user':user,'all_answer':new,'article':all_art})
    else:
        user = request.user
        all_art = Article.objects.filter(user=user)
        if all_art:
            for a in all_art:
                all_answer = Answer.objects.filter(article_id=a)
                for i in all_answer:
                    i.new_answer = False
                    i.save()
        return render_to_response('no_new_msg.html')


def view_all_attention(request):                 #在view_all页面点关注#
    id = request.GET["id"]
    art = Article.objects.get(id=id)
    add_attention = Friendship(
        to_friend=art.user,
        from_friend=request.user
    )
    add_attention.save()
    all_objects = Article.objects.all()
    username = request.session['username']
    attentioned_author = Friendship.objects.filter(from_friend=request.user)
    return render_to_response('view_all.html', {'all_objects': all_objects, 'username': username,
                                                'attentioned_author': attentioned_author,'request.user':request.user})


def cancel_view_all_attention(request):                 #在view_all页面取消关注#
    id = request.GET["id"]
    art = Article.objects.get(id=id)
    delete_attention = Friendship.objects.get(to_friend=art.user,from_friend=request.user)
    delete_attention.delete()
    all_objects = Article.objects.all()
    username = request.session['username']
    attentioned_author = Friendship.objects.filter(from_friend=request.user)
    return render_to_response('view_all.html', {'all_objects': all_objects, 'username': username,
                                                'attentioned_author': attentioned_author,'request.user':request.user})


def article_attention(request):                 #在article页面点关注#
    id = request.GET["id"]
    one = Article.objects.get(id=id)
    add_attention = Friendship(
        to_friend=one.user,
        from_friend=request.user
    )
    add_attention.save()

    all_answer = Answer.objects.filter(article_id=one)
    poll_num = one.poll_number
    exist = Poll.objects.filter(article=id, user=request.user)
    if exist:
        has_polled = True
    else:
        has_polled = False
    if exist:
        has_polled = True
    else:
        has_polled = False
    return render_to_response('article.html', {'article': one, 'all_answer': all_answer, 'poll_num': poll_num,
                                               'has_polled': has_polled})



def personal_inf(request):#统计信息
    id = request.user.id
    inf = auth_profile.objects.filter(user=id,
                                      Personality_signature='这个人很懒')
    return render_to_response('personal_inf.html',{'inf':inf})













