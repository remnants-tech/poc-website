from django.shortcuts import render
from django.http import HttpResponse

from .models import UserProfile,UserProfileDao

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def log_in(request):
    return render(request, 'log-in.html')

def sign_up(userInfo):
    sampleUser = UserProfile(userInfo.body)
    sampleUser.updateInfo()
    UserProfileDao.storeInfo(sampleUser)
    return HttpResponse('user created successfully')

 #   greeting = Greeting()
  #  greeting.save()

   # greetings = Greeting.objects.all()

    #return render(request, 'db.html', {'greetings': greetings})

