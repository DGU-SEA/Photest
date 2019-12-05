from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

#  유저 밑에 프로필 을 붙여서 보여주려고 이를 상속받음
class ProfileInline(admin.StackedInline):
    model = Profile
    con_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# 기존의 User의 등록을 취소했다가 User와 ProfileInline을 붙임.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)