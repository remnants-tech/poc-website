from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import UserProfile,UserProfileDao,ChurchProfileDao

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def log_in(request):
    return render(request, 'log-in.html')

def sign_up(userInfo):
    sampleUser = UserProfile(userInfo.body)
    sampleUser.updateInfo()
    sampleUser.enableDao()
    sampleUser.dao.initiateConn()
    if (sampleUser.dao.checkDuplicate("ID",sampleUser.ID)):
        return HttpResponse('ID already exists')
    if (sampleUser.dao.checkDuplicate("Email",sampleUser.Email)):
        return HttpResponse('Email already exists')
    sampleUser.dao.storeInfo(sampleUser.__dict__)
    sampleUser.dao.commit()
    sampleUser.dao.close()
    return HttpResponse('user created successfully')

def pull_churches(request):
    churchDao = ChurchProfileDao()
    churchDao.initiateConn()
    churchNames = churchDao.pullChurchName()
    churchNames = json.dumps(churchNames)
    return HttpResponse((churchNames))
    


 #   greeting = Greeting()
  #  greeting.save()

   # greetings = Greeting.objects.all()

    #return render(request, 'db.html', {'greetings': greetings})

