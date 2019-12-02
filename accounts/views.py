from django.shortcuts import render, redirect
# from django.http.response import HttpResponseRedirect
# from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import * 

def join(request):

    if request.method == "POST":

        username = request.POST["username"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        email=request.POST["email"]

        if User.objects.filter(username=username).exists() :
            return render(request, 'accounts/join.html', { 'is_used' : "중복된 ID 입니다."})

        if (username == "") or (password1 == "") or (password2 == "") or (email == ""):
            return render(request, 'accounts/join.html', { 'is_used' : "모든 필드를 입력해주세요."})

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
        return render(request, 'accounts/join.html', {'is_used' : "패스워드가 일치하지 않습니다."})
    return render(request, 'accounts/join.html', {})

def logout(request):
    auth.logout(request)  
    return redirect('/')   

def mypage(request):
    if not request.user.is_authenticated:
        print("usernone")
        return redirect('/')
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'accounts/mypage.html', {})