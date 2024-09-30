from django.contrib import admin
from .models import Image, Video, Category

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('categories',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('categories',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category)