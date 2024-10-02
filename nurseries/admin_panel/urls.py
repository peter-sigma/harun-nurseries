from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('login/', admin_login_view, name='admin_login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='admin_dashboard'),
    
     path('manage-images/', manage_images, name='manage_images'),
     path('add-image/', add_image, name='add_image'),
     path('view-images/', view_images, name='view_images'),
    path('manage-categories/', manage_categories, name='manage_categories'),
    path('add-category/', add_category, name='add_category'),
    path('update-image/<int:image_id>/', update_image, name='update_image'),
    path('delete-image/<int:image_id>/', delete_image, name='delete_image'),
     path('view-categories/', view_categories, name='view_categories'),
    path('update-category/<int:category_id>/', update_category, name='update_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
]