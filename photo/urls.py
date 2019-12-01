from django.urls import path
from .views import PhotoList, PhotoDelete, PhotoDetail, PhotoUpdate, PhotoCreate

from . import views
from .views import main, board, best, hashtag_board, logined_main

#app_name="photo
app_name="photo"
urlpatterns = [

    path("photo_create/", PhotoCreate.as_view(), name='create'),
    path("photo_detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path("photo_delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("photo_update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path('', views.main, name='main'),
    path('photo_list/', PhotoList.as_view(), name='photo_list'),
    path('best/', views.best, name='best'),
    path('hashtag_board', views.hashtag_board, name='hashtag_board'),
    path('mypage/', views.mypage, name='mypage'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('detail/', views.detail, name='detail'),
    path('logined_main/', views.logined_main, name = 'logined_main'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
