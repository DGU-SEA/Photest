from django.db import models
from django.contrib.auth.models import User

# Django에서 제공하는 User 모델을 그대로 사용하며, 추가적인 필드를 덧붙이기 위해 Profile을 사용
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reportCnt = models.IntegerField(default=0)
    rewardCnt = models.IntegerField(default=0)
