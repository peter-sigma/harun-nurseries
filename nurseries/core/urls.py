from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    # path('about', about, name='about'),
    path('images/', image_list, name='image_list'),
    path('images/category/<int:category_id>/', image_list, name='image_list_by_category'),
    path('videos/', video_list, name='video_list'),
    path('videos/category/<int:category_id>/', video_list, name='video_list_by_category'),
]