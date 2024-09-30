from django.shortcuts import render
from admin_panel.models import Image, Video, Category

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def image_list(request, category_id=None):
    categories = Category.objects.all()
    images = Image.objects.all()
    if category_id:
        images = images.filter(categories__id=category_id)
    return render(request, 'core/image_list.html', {'images': images, 'categories': categories})

def video_list(request, category_id=None):
    categories = Category.objects.all()
    videos = Video.objects.all()
    if category_id:
        videos = videos.filter(categories__id=category_id)
    return render(request, 'core/video_list.html', {'videos': videos, 'categories': categories})
