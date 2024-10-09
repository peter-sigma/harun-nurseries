from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import AdminLoginForm
from django.contrib.auth.decorators import login_required
from .models import Image, Video, Category


def admin_login_view(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        return redirect(reverse('admin_panel:admin_dashboard'))

    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect(reverse('admin_panel:admin_dashboard'))
            else:
                messages.error(request, 'Invalid credentials or insufficient privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()

    return render(request, 'admin_panel/login.html', {'form': form})


@login_required
def dashboard(request):
    total_images = Image.objects.count()
    total_videos = Video.objects.count()
    total_categories = Category.objects.count()
    categories = Category.objects.all()

    recent_images = Image.objects.order_by('-id')[:5]  # Show 5 most recent images
    recent_videos = Video.objects.order_by('-id')[:5]  # Show 5 most recent videos

    context = {
        'total_images': total_images,
        'total_videos': total_videos,
        'total_categories': total_categories,
        'categories': categories,
        'recent_images': recent_images,
        'recent_videos': recent_videos,
    }

    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_panel:admin_login')


@login_required
def manage_images(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES['image_file']
        category_id = request.POST.get('category')  # Changed to single category
        category = get_object_or_404(Category, id=category_id)

        new_image = Image.objects.create(title=title, image_file=image_file, category=category)
        new_image.save()

        return redirect('admin_panel:manage_images')

    images = Image.objects.all()
    total_images = Image.objects.count()
    categories = Category.objects.all()  # Fetch categories to display in the form
    return render(request, 'admin_panel/manage_images.html', {'images': images, 'categories': categories, 'total_images': total_images})


@login_required
def add_image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES['image_file']
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)

        # Check if an image with the same title exists
        if Image.objects.filter(title=title).exists():
            categories = Category.objects.all()
            error_message = "An image with this title already exists. Please choose a different title."
            return render(request, 'admin_panel/add_image.html', {
                'categories': categories,
                'error_message': error_message
            })

        # If no existing title, create the new image
        new_image = Image.objects.create(title=title, image_file=image_file, category=category)
        new_image.save()

        return redirect('admin_panel:manage_images')

    categories = Category.objects.all()
    return render(request, 'admin_panel/add_image.html', {'categories': categories})



@login_required
def update_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')  # Changed to single category
        print(category_id)
        category = get_object_or_404(Category, id=category_id)

        image.title = title
        if 'image_file' in request.FILES:
            image.image_file = request.FILES['image_file']
        image.category = category  # Set the single category for the image
        image.save()

        return redirect('admin_panel:view_images')

    categories = Category.objects.all()
    return render(request, 'admin_panel/update_image.html', {'image': image, 'categories': categories})


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('admin_panel:view_images')


@login_required
def manage_categories(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        Category.objects.create(name=category_name, description=description)
        return redirect('admin_panel:manage_categories')

    categories = Category.objects.all()
    return render(request, 'admin_panel/manage_categories.html', {'categories': categories})


@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')

        # Check if a category with the same name already exists
        if Category.objects.filter(name=category_name).exists():
            error_message = "A category with this name already exists. Please choose a different name."
            return render(request, 'admin_panel/add_category.html', {
                'error_message': error_message,
                'category_name': category_name,
                'description': description
            })

        # Create the category if no duplicate exists
        Category.objects.create(name=category_name, description=description)
        return redirect('admin_panel:view_categories')

    return render(request, 'admin_panel/add_category.html')



@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('category_name', category.name)
        category.description = request.POST.get('description', category.description)  # Update description
        category.save()
        return redirect('admin_panel:view_categories')

    return render(request, 'admin_panel/update_category.html', {'category': category})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('admin_panel:view_categories')


@login_required
def view_images(request):
    images = Image.objects.all()
    return render(request, 'admin_panel/view_images.html', {'images': images})


@login_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/view_categories.html', {'categories': categories})


@login_required
def manage_videos(request):
    total_videos = Video.objects.count()
    return render(request, 'admin_panel/manage_videos.html', {'total_videos': total_videos})


@login_required
def add_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        video_file = request.FILES['video_file']
        category_id = request.POST.get('category')

        # Check if a video with the same title already exists
        if Video.objects.filter(title=title).exists():
            error_message = "A video with this title already exists. Please choose a different title."
            categories = Category.objects.all()  # Fetch categories to redisplay the form
            return render(request, 'admin_panel/add_video.html', {
                'error_message': error_message,
                'title': title,
                'categories': categories,
                'category_id': category_id
            })

        # Proceed to save the new video
        category = get_object_or_404(Category, id=category_id)
        video = Video.objects.create(title=title, video_file=video_file, category=category)
        video.save()

        return redirect('admin_panel:view_videos')

    categories = Category.objects.all()
    return render(request, 'admin_panel/add_video.html', {'categories': categories})



@login_required
def update_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        video.title = request.POST.get('title', video.title)
        if 'video_file' in request.FILES:
            video.video_file = request.FILES['video_file']
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)

        video.category = category  # Set the single category for the video
        video.save()

        return redirect('admin_panel:view_videos')

    categories = Category.objects.all()
    return render(request, 'admin_panel/update_video.html', {'video': video, 'categories': categories})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect('admin_panel:view_videos')


@login_required
def view_videos(request):
    videos = Video.objects.all()
    return render(request, 'admin_panel/view_videos.html', {'videos': videos})