from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
class hashtag(models.Model):
    # 태그 이름, 태그된 횟수, 좋아요 한 유저 수, 지정날짜
    tagName = models.CharField(max_length=20,blank=False, primary_key=True)
    tagCnt = models.IntegerField(default=0)
    likeCnt = models.IntegerField(default=0)
    tagDate = models.DateField(blank=True, null = True)




