from django.shortcuts import render, redirect, HttpResponse
from .models import User, Secret
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'whisper/index.html')

def secrets(request):
    if 'userid' not in request.session:
        return redirect ("/")
    return render(request, 'whisper/secrets.html')

def whisper(request):
    if 'userid' not in request.session:
        return redirect ("/")
    if request.method == "POST":
        user = User.objects.get(id= request.session['userid'])
        newmessage = Secret.objects.secreteval(request.POST['message'], user)
        if newmessage[0] == False :
            for each in newmessage[1]:
                messages.error(request, each)
            return redirect('/secrets')
        if newmessage[0]==True:
            print newmessage[1]
            return redirect('/secrets')

def like(request):
    if request.method == "POST":
        newlike = Secret.objects.get()
        newmlike.like.add(id = request.session['userid'])
    else:
        message.add(request, messageINFO, "Nice try")
    return redirect('/secrets')

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
    # if 'userid' in request.session:
    #     return redirect('/success')
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
