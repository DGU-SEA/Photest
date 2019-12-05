from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Photo
from .models import User
from accounts.models import Profile
from hashtag.models import hashtag
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from datetime import date, timedelta
from django.db import connection
import json
from urllib.parse import urlparse
from django.core.files import File
import urllib.request
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from django.utils.dateparse import parse_date


def main(request):
    print('main')
    global hashtag
    global Photo
    hashtags = hashtag.objects.all()

    # # ------------------------- 오늘의 해시태그 & 어제의 해시태그 처리 ----------------------------
    todaytag = ""
    todayDate = str(date.today())
    # todayDate = str(datetime.now().year)+ '-' + str(datetime.now().month)+ '-' + str(datetime.now().day)

    yesterdaytag = ""
    today = date.today()
    yesterday = str(date.today() - timedelta(1))

    for h in hashtag.objects.all() :
        if(str(h.tagDate) == todayDate) : 
            todaytag = h.tagName
        
        if(str(h.tagDate) == yesterday) :
            yesterdaytag = h.tagName
    # print(todaytag)
    # ------------------------- 어제의 해시태그 -> photo에서 hashtag필드에 어제 해시태그 포함한 것들중에서 5개 전달 ----------------------------
    Photos = Photo.objects.all().order_by('-like')
    BestPhotos = list()

    index = 0
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == yesterdaytag) : 
                BestPhotos.append(p)
                index += 1
                break
            if(index == 5) : break

    print(len(BestPhotos))
    for p in BestPhotos :
        print(p.image)

    return render(request, 'photo/main.html', context={'todaytag' : todaytag, 'yesterdaytag' : yesterdaytag, 'BestPhotos' : BestPhotos})
    
def best(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    yesterday = date.today() - timedelta(1)
    # print(str(yesterday))

    days = [yesterday]
    tags = []
    bestPhotos =[]
    temp = 0
    for i in range(1, 7):
        temp = yesterday - timedelta(i)
        days.append(temp)

    # print(days)

    for i in range(0, 7):
        for h in hashtag.objects.all():
            if (h.tagDate == days[i]):
                tags.append(h.tagName)
                # print(h.tagName)

    photos = Photo.objects.all().order_by('-like')

    index = 0
    for i in tags :
        for p in photos :
            if (p.hashtag['tag'] == i):
                bestPhotos.append(p)
                # p.author
                index += 1
                if index == 5 :
                    break
    # print(bestPhotos)
    return render(request, 'photo/best.html', context={'days': days, 'tags': tags, 'bestPhotos': bestPhotos})
    
def hashtag_board(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/hashtag_board.html', {}) #, {'posts': posts}

def upload(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/upload.html', {})


def edit_profile(request):
#best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
 return render(request, 'photo/edit_profile.html', {})

def detail(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    model = Photo
    return render(request, 'photo/detail.html', {})

def search_list(request):
    print('search list')
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()
    search = request.GET.get('search', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == search) : 
                PhotosWithHashtag.append(p)

    print(PhotosWithHashtag)
    print(search)

    return render(request, 'photo/search_list.html', {
        'PhotosWithHashtag' : PhotosWithHashtag,
        'search' : search
    })


def today_hashtag_click(request) :
    print('today hashtag click')
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()

    global hashtag
    hashtags = hashtag.objects.all()
    todaytag = ""
    todayDate = str(date.today())

    for h in hashtag.objects.all() :
        if(str(h.tagDate) == todayDate) : 
            todaytag = h.tagName

    print(todaytag)
    
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == todaytag) :
                PhotosWithHashtag.append(p)
    
    return render(request, 'photo/search_list.html', {
        'PhotosWithHashtag' : PhotosWithHashtag,
        'search' : todaytag
    })

def yesterday_hashtag_click(request) :
    print('yesterday hashtag click')
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()

    yesterdaytag = ""
    today = date.today()
    yesterday = str(date.today() - timedelta(1))

    for h in hashtag.objects.all() :        
        if(str(h.tagDate) == yesterday) :
            yesterdaytag = h.tagName
    
    print(yesterdaytag)
    
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == yesterdaytag) :
                PhotosWithHashtag.append(p)
    

    return render(request, 'photo/search_list.html', {
        'PhotosWithHashtag' : PhotosWithHashtag,
        'search' : yesterdaytag
    })

def board_search(self, request, *args, **kwargs) :
    print('board search')
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()

    search = request.GET.get('search', '')
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == search) :
                PhotosWithHashtag.append(p)
    
    return render(request, 'photo/search_list.html', {
        'PhotosWithHashtag' : PhotosWithHashtag,
        'search' : search
    })

def photo_list(request) :
    print('photo list')
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()

    global hashtag
    hashtags = hashtag.objects.all()
    todaytag = ""
    todayDate = str(date.today())

    for h in hashtag.objects.all() :
        if(str(h.tagDate) == todayDate) : 
            todaytag = h.tagName

    print(todaytag)
    
    for p in Photos :
        PhotosWithHashtag.append(p)
    
    return render(request, 'photo/photo_list.html', {
        'PhotosWithHashtag' : PhotosWithHashtag,
        'todaytag' : todaytag
    })

def photo_insert(request) :
    # if request.method == "POST":
    #     print("**********************************************************************")
    print('photo create')
    username = request.user
    Users = User.objects.all()
    authorid = ""

    for u in Users :
        if(str(u.username) == str(username)) :
            authorid = u
    # print(authorid)
    # print("request.FILES : "+ request.FILES['image'])
    image = request.FILES['image']
    # print(image)
    # tempurl = 'timeline_photo/2019/12/04/'
    # tempurl += str(image)
    # tempurl += str(dateemonth) 
    # tempurl += '/'
    # tempurl += str(date.day)
    # tempurl += '/'
    # tempurl += str(image)

    # print(tempurl)
    # image = "https://cdn.pixabay.com/photo/2016/08/27/11/17/bag-1623898_960_720.jpg"

    hashtag1 = request.POST.get('hashtag1', '')
    hashtag2 = request.POST.get('hashtag2', '')
    hashtag3 = request.POST.get('hashtag3', '')
    # hashtag1 = request.POST['hashtag1']
    # hashtag2 = request.POST['hashtag2']
    # hashtag3 = request.POST.get('hashtag3')

    
    print(hashtag1)
    print(hashtag2)
    print(hashtag3)

    hashtag = {
        'tag' : []
    }

    if(hashtag1 != "") :
        hashtag['tag'].append(hashtag1)
    if(hashtag2 != "") :
        hashtag['tag'].append(hashtag2)
    if(hashtag3 != "") :
        hashtag['tag'].append(hashtag3)

    print(hashtag['tag'])
    
    # myfile = request.FILES['image']
    # fs = FileSystemStorage('photo/media/timeline_photo/')
    # filename = fs.save(myfile.name, myfile)
    # uploaded_file_url = fs.url(filename)
    # uploaded_file_url = fs.url(tempurl)

    # print(uploaded_file_url)

    print(type(authorid))
    print(type(image))
    print(type(hashtag))
    # print(type(Photo.objects.get(username)))

    data = Photo.objects.create(author = authorid, image = image, hashtag = hashtag)

    # print(request.POST['path'])
    return HttpResponseRedirect('/photo_list/')



def reward(request) :
    print('reward')
    # 사용자가 지정한 날짜, 해시태그 이름, 해시태그 테이블에 추가 혹은 수정
   
    global hashtag
    hashtags = hashtag.objects.all()
    requestdate = request.GET.get('user_date', '')
    convertdate = datetime.strptime(requestdate, "%Y-%m-%d")
  
    requesttag = request.GET.get('user_hashtag','')
    username = request.user
    Users = User.objects.all()
    authorid = ""

    for u in Users :
        if(str(u.username) == str(username)) :
            authorid = u.id

    set_instance = Profile.objects.get(user = authorid)
    set_instance.rewardCnt = 0
    set_instance.save()    
    
    print(requestdate, requesttag, username)

    index =0
    temp =""
    length = len(hashtags)
    for h in hashtags :
        #있으면 update
        if(h.tagName == requesttag) :
            temp = convertdate.date()
            h.tagDate = temp
            
            update_instance = hashtag.objects.get(tagName = requesttag)
            update_instance.tagDate = temp
            update_instance.save()
            break

        index += 1
    
    print(index, length)
    #없으면 insert
    if(index == length) :
        print('insert')
        insert_instance = hashtag(tagName = requesttag, tagDate = convertdate.date())
        insert_instance.save()

    

    return render(request, 'accounts/mypage.html', { 'Message' : 'reward complete' })


class PhotoList(ListView) :
    print('PhotoList')
    model = Photo
    emplate_name_suffix='_list'

    def search(request) :
        # search = request.POST.['search']
        print(' def fun inside')
        return render(request, 'photo/photo_list.html', {"PhotosWithHashtag" : PhotosWithHashtag})


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author','text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix='_detail'


from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

class PhotoLike(ListView):
    model = Photo
    template_name_suffix='_like'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/') # 로그인 되어 있지 않으면 메인 화면으로 보내기
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all(): # user가 이미 좋아요 한 사람 중에 있으면 클릭했을 때 지워지도록 
                    photo.like.remove(user) 
                else: # 새로운 user가 좋아요 한 것이라면 +1
                    photo.like.add(user) 
            
    
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
