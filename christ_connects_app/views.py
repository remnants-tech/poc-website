from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
import json
from .models import UserProfile,UserProfileDao,ChurchProfile, ChurchProfileDao

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def log_in(request):
    return render(request, 'log_in.html')

def sign_up(userInfo):
    newUser = UserProfile(userInfo.body)
    return HttpResponse(newUser.saveUser())

def user_sign_up(request):
    return render(request, 'user_sign_up.html')
    

def pull_churches(request):
    churchDao = ChurchProfileDao()
    churchDao.initiateConn()
    churchNames = churchDao.pullChurchName()
    churchNames = json.dumps(churchNames)
    return HttpResponse((churchNames))

def user_church_reg(churchInfo):
    newChurch = ChurchProfile(churchInfo.body)
    newChurch.saveChurch()
    

def account_confirm(request):
    return render(request, 'account_confirm.html')
    

 #   greeting = Greeting()
  #  greeting.save()

   # greetings = Greeting.objects.all()

    #return render(request, 'db.html', {'greetings': greetings})

