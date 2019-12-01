from django.shortcuts import render, redirect
# from django.http.response import HttpResponseRedirect
# from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import * 

def join(request):
    if request.method == "POST":
        username = request.POST["username"]
        if User.objects.filter(username=username).exists() :
            return render(request, 'accounts/join.html', { 'is_used' : "중복된 ID 입니다."})
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
            	email=request.POST["email"])
            profile = Profile(user=user)
            profile.save()
            auth.login(request,user)
            # return HttpResponseRedirect(reverse('photo/main'))
            return redirect('/')  
        return render(request, 'accounts/join.html', {})
    return render(request, 'accounts/join.html', {})

def logout(request):
    auth.logout(request)  
    return redirect('/')   