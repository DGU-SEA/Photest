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

    # ------------------------- 오늘의 해시태그 & 어제의 해시태그 처리 ----------------------------
    todaytag = ""
    todayDate = str(datetime.now().year)+ '-' + str(datetime.now().month)+ '-' + str(datetime.now().day)
    dbDate = ""

    yesterdaytag = ""
    today = date.today()
    yesterday = str(date.today() - timedelta(1))

    for h in hashtag.objects.all() :
        if(str(h.tagDate) == todayDate) : 
            todaytag = h.tagName
        
        if(str(h.tagDate) == yesterday) :
            yesterdaytag = h.tagName
    print(todaytag)
    # ------------------------- 어제의 해시태그 -> photo에서 hashtag필드에 어제 해시태그 포함한 것들중에서 5개 전달 ----------------------------
    Photos = Photo.objects.all().order_by('-like')
    print(Photos)

    for p in Photos :
        print(p.like.all())

    return render(request, 'photo/main.html', context={'todaytag' : todaytag, 'yesterdaytag' : yesterdaytag})
    
def board(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/board.html', {}) #, {'posts': posts}

def best(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/best.html', {}) #, {'posts': posts}
    
def hashtag_board(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/hashtag_board.html', {}) #, {'posts': posts}

def upload(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/upload.html', {})

def mypage(request):
    #best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
    return render(request, 'photo/mypage.html', {})

def edit_profile(request):
#best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
 return render(request, 'photo/edit_profile.html', {})

def logined_main(request):
#best = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')*/
 return render(request, 'photo/logined_main.html', {})


class PhotoList(ListView):
    model = Photo
    template_name_suffix='_list'

class PhotoCreate(CreateView):
    model = Photo
    
    fields = ['author','text', 'image', 'hashtag']
    template_name_suffix = '_create'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.author_id=self.request.user.author_id
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
