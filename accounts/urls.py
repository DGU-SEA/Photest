from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.join, name='join'),
    path('mypage/', views.mypage, name='mypage'),
    path('report/', views.report, name='report'),
    path('reward/', views.reward, name='reward'),
]


