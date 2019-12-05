from django.urls import path
from .views import PhotoList, PhotoDelete, PhotoDetail, PhotoUpdate, PhotoLike

from . import views
from .views import main, best, hashtag_board, search_list, reward

app_name="photo"
urlpatterns = [
    path("photo_detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path("photo_delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("photo_update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path('', views.main, name='main'),
    path('photo_list/', views.photo_list, name='photo_list'),
    path('best/', views.best, name='best'),
    path('hashtag_board', views.hashtag_board, name='hashtag_board'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('detail/', views.detail, name='detail'),
    path("like/<int:photo_id>/", PhotoLike.as_view(), name = 'like'),
    path('upload/',views.upload, name='upload'),
    path('search/', views.search_list, name='search'),
    path('today_hashtag_search/', views.today_hashtag_click, name='today_hashtag_search'),
    path('yesterday_hashtag_search/', views.yesterday_hashtag_click, name='yesterday_hashtag_search'),
    path('photo_inserts/', views.photo_insert, name='photo_insert'),
    path('reward/', views.reward, name = 'reward')
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)