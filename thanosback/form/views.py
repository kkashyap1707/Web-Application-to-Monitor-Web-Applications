from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Userdata,User_url_info
from .forms import Formsignup
from django.shortcuts import redirect
import form.stack_build as infra
from django import template


def signup_form(request):
    return render(request,'form/signup/signup2.html')

def login_form(request):
    return render(request,'form/login/login1.html')

def entry_signup_data(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            post=Userdata()
            post.email= request.POST.get('email')
            post.password= request.POST.get('password')
            post.user_name=request.POST.get('user_name')
            post.save()
            return render(request, 'form/login/login1.html')  

def index(request):
    return render(request,'form/landing.html')

def entry_form(request):
    return render(request,'form/user/entry1.html')

def entry_login_data(request):
    if request.method == 'POST':
        if request.POST.get('email') and request.POST.get('password'):
            email=request.POST.get('email')
            password=request.POST.get('password')
            result=Userdata.objects.all()
            flag=0
            for i in result:
                if i.email==email and i.password==password:
                    flag=1
                    break
                else:
                    flag=0
            if flag==1:
                    return redirect('/form/user/check/'+str(i.id))
            else:
                return redirect('/form/login')

def entry_form_data(request):
    if request.method=='POST':
        ids=request.POST.get('value')
        post=User_url_info()
        post1=Userdata.objects.all()
        for i in post1:
            if i.id == int(ids):
                post.userid=i
                break
        post.url=request.POST.get('url')
        post.subscribers=request.POST.get('subscriber')
        post.status=request.POST.get('status')
        post.access=request.POST.get('access')
        post.cron=request.POST.get('cron')
        subscribers=post.subscribers.split(",")
        print(i.user_name)
        obj=infra.infrastructure(post.status,post.access,i.user_name,post.cron,post.url,subscribers)
        obj.createTopic()
        obj.attachSubscriber()
        obj.createLambdaStack()
        post.save()
        ids=request.POST.get('value')
        response=redirect('/form/user/check/'+ids)
        return response

def data_display(request,objects):
    result=User_url_info.objects.all()
    url=[]
    subscriber=[]
    access=[]
    status=[]
    cron=[]
    flag=0
    for i in result:
        if str(i.userid.id) == str(objects):
            url.append(i.url)
            subscriber.append(i.subscribers)
            access.append(i.access)
            status.append(i.status)
            cron.append(i.cron)
            flag=1
    if flag==1:
        context={
            'url':url,
            'subscriber':subscriber,
            'access':access,
            'status':status,
            'cron':cron,
            
        }
        return render(request,'form/user/user_filled.html',context)
    else:
        context={
            'id':objects,
        }
        return render(request,'form/user/entry1.html',context)