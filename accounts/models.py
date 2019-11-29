from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reportCnt = models.IntegerField(default=0)
    likeCnt = models.IntegerField(default=0)
