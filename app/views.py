from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import  reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registeration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            send_mail('REGISTERTAION','registerdone succesfully','sairanjansahu2000@gmail.com',[NSUO.email],fail_silently=False)
            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')

    return render(request,'registeration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home')) 
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    uo=User.objects.get(username=username)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}

    return render(request,'display_profile.html',d)
@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('PASSWORD CHANGED succesfully')

    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        luo=User.objects.filter(username=username)
        if luo:
            uo=luo [0]
            uo.set_password(password)
            uo.save()
        else:

            
            return HttpResponse('user name is not available')
        return HttpResponse('PASSWORD changed succesfully')
    return render(request,'forgot_password.html')
    




