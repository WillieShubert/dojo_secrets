from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'whisper/index.html')

def secrets(request):
    if 'userid' in request.session:
        allsecrets = Secret.objects.all().order_by('-id') [:5]
        context ={
            "secrets": allsecrets,
            "currentuser": User.objects.get(id= request.session['userid'])
        }
        return render(request, 'whisper/secrets.html', context)
    else:
        return redirect('/')

def process(request):
    if request.method =='GET':
        return redirect('/')
    result= Secret.objects.validate(request.POST['message'], request.session['userid'])
    if result[0]:
        messages.info(request, result[1])
        return redirect('/secrets')
    messages.error(request, result[1])
    return redirect('/secrets')

def newlike(request, id, sentby):
    result= Secret.objects.newlike(id, request.session['userid'])
    if result[0]==False:
        message.error(request, result[1])
    if sentby=="sec":
        return redirect ("/secrets")
    else:
        return redirect('/popular')

def delete(request, id, sentby):
    print "deleting", id
    result = Secret.objects.deleteLike(id, request.session['userid'])
    if result[0]==False:
        message.error(request, result[1])
    if sentby=="sec":
        return redirect ("/secrets")
    else:
        return redirect('/popular')

def popular(request):
    if 'userid' in request.session:
        allsecrets= Secret.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')
        context = {
            "secrets": allsecrets,
            "currentuser": User.objects.get(id=request.session['userid'])
        }
        return render(request,'whisper/popular.html', context)
    else:
        return redirect ('/')

def register(request):
    if request.method == 'GET':
        return redirect ('/')
    newuser = User.objects.validate(request.POST)
    print newuser
    if newuser[0] == False:
        for each in newuser[1]:
            messages.error(request, each) #for each error in the list, make a message for each one.
        return redirect('/')
    if newuser[0] == True:
        messages.success(request, 'Well done')
        request.session['userid'] = newuser[1].id
        return redirect('/secrets')

def login(request):
    if 'userid' in request.session:
        return redirect('/secrets')
    if request.method == 'GET':
        return redirect('/')
    else:
        user = User.objects.login(request.POST)
        print user
        if user[0] == False:
            for each in user[1]:
                messages.add_message(request, messages.INFO, each)
            return redirect('/')
        if user[0] == True:
            messages.add_message(request, messages.INFO,'Welcome, You are logged in!')
            request.session['userid'] = user[1].id
            return redirect('/secrets')

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    print "*******"
    print request.session['userid']
    del request.session['userid']
    return redirect('/')
