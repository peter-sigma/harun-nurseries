from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('images/', views.image_list, name='image_list'),
    path('images/category/<int:category_id>/', views.image_list, name='image_list_by_category'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/category/<int:category_id>/', views.video_list, name='video_list_by_category'),
]