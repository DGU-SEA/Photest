from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import * 
from django.contrib.auth.hashers import check_password
from photo.models import Photo
from hashtag.models import hashtag

# join, logout, mypage, report, reward 함수

def join(request):
    if request.method == "POST":
        # html 으로부터 넘어온 모든 값
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]

        # 중복 ID 체크
        if User.objects.filter(username=username).exists() :
            return render(request, 'accounts/join.html', { 'is_used' : "중복된 ID 입니다."})

        # 모든 필드 미작성 시
        if (username == "") or (password1 == "") or (password2 == "") or (email == ""):
            return render(request, 'accounts/join.html', {'is_used':"모든 필드를 입력해주세요."})

        # 패스워드 불일치
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
            	email=request.POST["email"] )
            profile = Profile(user=user)
            profile.save()
            auth.login(request,user)
            return redirect('/')  
        return render(request, 'accounts/join.html', {'is_used' : "패스워드가 일치하지 않습니다."})
    return render(request, 'accounts/join.html', {})


def logout(request):
    auth.logout(request)  
    return redirect('/')   

def mypage(request):
    global Photo

    # 로그인 시에만 mypage 접근 가능
    if not request.user.is_authenticated:
        print("user is not authenticated")
        return redirect('/')

    allphotos = Photo.objects.all().order_by('-like')
    photos = []

    for p in allphotos:
        if request.user == p.author :
            # print(p.image.url)
            photos.append(p)

    # 정보 수정 시
    if request.method == "POST":
        password=request.POST["password"]
        email=request.POST["email"]

        if (password != "" and email != "") or password != "" :
            request.user.set_password(password)
            request.user.save() 
            return redirect('/')  
        if email != "":
            request.user.email = email
            request.user.save()
            return render(request, 'accounts/mypage.html', {'photos' : photos})
        return render(request, 'accounts/mypage.html', {'photos' : photos})

    return render(request, 'accounts/mypage.html', {'photos' : photos})

# 신고받은 사진의 작성자 신고받은 횟수 +1
def report(request) :
    if request.method == "GET":
        author = request.GET['author']
        user = User.objects.get(username=author)
        user.profile.reportCnt += 1
        user.profile.save()
        return HttpResponseRedirect(request.GET['path'])

# 관리자가 날짜를 선택하면 해당 날짜 1-5등의 reward +1
def reward(request) :
    if request.method == "GET":
        date = request.GET['user_date']
        tag = ""

        for h in hashtag.objects.all():
            if (str(h.tagDate) == date):
                tag = h.tagName
                print("tag : " + tag)

        photos = Photo.objects.all().order_by('-like')
        bestPhotos =[]
        index = 0

        for p in photos :
            for h in p.hashtag['tag']:
                # print(p.hashtag['tag'])
                if (h == tag):
                    bestPhotos.append(p)
                    index += 1
                if index == 5:
                    break

        for bp in bestPhotos:
            user = User.objects.get(username=bp.author)
            print(user.profile.rewardCnt)
            user.profile.rewardCnt += 1
            print(user.profile.rewardCnt)
            user.profile.save()

        return render(request, 'accounts/mypage.html', {'bestPhotos': bestPhotos})
