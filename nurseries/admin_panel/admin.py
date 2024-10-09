from django.contrib import admin
from .models import Image, Video, Category

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')  # Display title and category (singular)
    search_fields = ('title',)  # Enable search by title

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')  # Display title and category (singular)
    search_fields = ('title',)  # Enable search by title

admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category)