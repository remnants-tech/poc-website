from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
import json
from .models import UserProfile,UserProfileDao,ChurchProfile, ChurchProfileDao
import urllib.parse

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def log_in(request):
    return render(request, 'log_in.html')

def sign_up(userInfo):
    parsedUserInfo = urllib.parse.unquote_plus(str(userInfo.body))
    newUser = UserProfile(parsedUserInfo)
    return HttpResponse(newUser.saveUser())

def user_sign_up(request):
    return render(request, 'user_sign_up.html')

def user_authentication(userAccountInfo):
    parsedUserAccountInfo = urllib.parse.unquote_plus(str(userAccountInfo.body))
    newUserDao = UserProfileDao()
    userAccountDict = newUserDao.urlToDict(parsedUserAccountInfo)
    return HttpResponse(newUserDao.authenticateUser(userAccountDict['pass'],userAccountDict['id']))
    

def pull_churches(request):
    churchDao = ChurchProfileDao()
    churchDao.initiateConn()
    churchNames = churchDao.pullChurchName()
    churchNames = json.dumps(churchNames)
    return HttpResponse((churchNames))

def user_church_reg(churchInfo):
    parsedChurchInfo = urllib.parse.unquote_plus(str(churchInfo.body))
    newChurch = ChurchProfile(parsedChurchInfo)
    return HttpResponse(newChurch.saveChurch())
    

def account_confirm(request):
    return render(request, 'account_confirm.html')

def church_lookup(request):
    return render(request, 'church_lookup.html')

def search_church_criteria(searchInput):
    parsedCriteria= urllib.parse.unquote_plus(str(searchInput.body))
    newChurchDao = ChurchProfileDao()
    criteriaDict = newChurchDao.urlToDict(parsedCriteria)
    criterion = list(criteriaDict.keys())[0]
    churchDict = newChurchDao.pullGeocodeByCriteria([criterion,criteriaDict[criterion]])
    newChurchDao.close()
    return HttpResponse(json.dumps(churchDict))
    
    
    
    
    
    

 #   greeting = Greeting()
  #  greeting.save()

   # greetings = Greeting.objects.all()

    #return render(request, 'db.html', {'greetings': greetings})

