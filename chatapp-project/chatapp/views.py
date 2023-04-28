from django.shortcuts import render,redirect
from .models import ChatRoom,ChatMessage
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from .forms import LoginForm
from  django.contrib.auth import authenticate,login

# Create your views here.
def UserLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username = data['username'],password = data['password'])
            
            if user is not None:
                login(request,user)
                return redirect('rooms/')
            else:
                return HttpResponse("Invalid Credentials")

    else:
        form = LoginForm()        
        context = {
            'form':form
        }
    return render(request,'chatapp/login.html',context)

def index(request):
    chatrooms = ChatRoom.objects.all()
    if request.method == 'POST':
        print(request)

    context = {
        'chatrooms':chatrooms
    }
    return render(request,'chatapp/index.html',context)

def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug = slug)
    messages = ChatMessage.objects.filter(room = chatroom)[0:30]
    context = {
        'chatroom':chatroom,
        'messages':messages
    }
    return render(request,'chatapp/room.html',context)