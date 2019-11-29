from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# from django.contrib.postgres.fields import JSONField


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # hashtag = models.JSONField(blank=True)
    
    # like = models.ManyToManyField(User, related_name='like_post', blank=True)
    # favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    def __str__(self): # admin 사이트 화면 표시 구현
        return "text : "+self.text

    class Meta: # ordering 정렬
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])


