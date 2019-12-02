from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Photo
from hashtag.models import hashtag
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from datetime import date, timedelta
from django.db import connection

def main(request):
    global hashtag
    global Photo
    hashtags = hashtag.objects.all()

    # # ------------------------- 오늘의 해시태그 & 어제의 해시태그 처리 ----------------------------
    todaytag = ""
    todayDate = str(datetime.now().year)+ '-' + str(datetime.now().month)+ '-' + str(datetime.now().day)
    dbDate = ""
    # print(todayDate)

    yesterdaytag = ""
    today = date.today()
    yesterday = str(date.today() - timedelta(1))
    # print(yesterday)

    for h in hashtag.objects.all() :
        if(h.tagDate == todayDate) : 
            todaytag = h.tagName
        
        if(str(h.tagDate) == yesterday) :
            yesterdaytag = h.tagName

    # print(todaytag)
    # ------------------------- 어제의 해시태그 -> photo에서 hashtag필드에 어제 해시태그 포함한 것들중에서 5개 전달 ----------------------------
    Photos = Photo.objects.all().order_by('-like')
    bestPhotos = list()

    index = 0
    for p in Photos :
        for t in p.hashtag['tag'] :
            if(t == yesterdaytag) : 
                bestPhotos.append(p)
                index += 1
                if(index == 5) : 
                    break

    return render(request, 'photo/main.html', context={'todaytag' : todaytag, 'yesterdaytag' : yesterdaytag, 'bestPhotos' : bestPhotos})
    
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
                index +1
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

class PhotoList(ListView):
    model = Photo
    template_name_suffix='_list'

    # 넘어오는 search 검색어 -> photo 모델에서 list 받아와서 hashtag 필드에 search 있는 애들 전달 
    Photos = Photo.objects.all()
    PhotosWithHashtag = list()
    # for p in Photos : 
        # print(p.hashtag)


class PhotoCreate(CreateView):
    model = Photo

    fields = ['author', 'image'] #'hashtag'
    template_name_suffix = '_create'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})


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

# class PhotoLikeList(ListView):
#     model = Photo
#     template_name = 'photo/photo_list.html'

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:  # 로그인확인
#             messages.warning(request, '로그인을 먼저하세요')
#             return HttpResponseRedirect('/')
#         return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

#     def get_queryset(self):
#         # 내가 좋아요한 글을 보여주
#         user = self.request.user
#         queryset = user.like_post.all()
#         return queryset

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
            # referer_url = request.META.get('HTTP_REFERER')
            # path = urlparse(referer_url).path
            return super(PhotoLike, self).get(request, *args, **kwargs)
    