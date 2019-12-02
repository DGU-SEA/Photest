from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import jsonfield

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to= 'timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    hashtag = jsonfield.JSONField(blank = True)
    like = models.IntegerField(User, blank=True)
    # favorite=models.IntegerField(User,blank=True, default=0)
   
    def __str__(self): # admin 사이트 화면 표시 구현
        return "text : "+self.text

    class Meta: # ordering 정렬
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])

