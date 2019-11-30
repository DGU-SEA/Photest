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

def main(request):
    global hashtag
    hashtags = hashtag.objects.all()
    print(hashtag.objects.all())
    print(datetime.now())

    todaytag = ""
    for hashtag in hashtag.objects.all() :
        if(hashtag.tagDate == datetime.now()) : 
            todaytag = hashtag.tagName
    
    return render(request, 'photo/main.html', {'todaytag' : "#sampleTag"})
    
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