from django.shortcuts import render
from django.shortcuts import render, redirect
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
    # Fetch data for images, videos, and categories
    total_images = Image.objects.count()
    total_videos = Video.objects.count()
    categories = Category.objects.all()

    # You can also include recent activities, such as recently uploaded images/videos
    recent_images = Image.objects.order_by('-id')[:5]  # Show 5 most recent images
    recent_videos = Video.objects.order_by('-id')[:5]  # Show 5 most recent videos

    context = {
        'total_images': total_images,
        'total_videos': total_videos,
        'categories': categories,
        'recent_images': recent_images,
        'recent_videos': recent_videos,
    }

    return render(request, 'admin_panel/dashboard.html', context)


@login_required  # Ensure that only logged-in users can access this view
def logout_view(request):
    logout(request)
    return redirect('admin_panel:admin_login') 


@login_required
def manage_images(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES['image_file']
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_ids)

        new_image = Image.objects.create(title=title, image_file=image_file)
        new_image.categories.set(categories)
        new_image.save()
        return redirect('admin_panel:manage_images')

    images = Image.objects.all()
    categories = Category.objects.all()  # Fetch categories to display in the form
    return render(request, 'admin_panel/manage_images.html', {'images': images, 'categories': categories})

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
def add_image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES['image_file']
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_ids)

        new_image = Image.objects.create(title=title, image_file=image_file)
        new_image.categories.set(categories)
        new_image.save()
        return redirect('admin_panel:manage_images')
    return redirect('admin_panel:manage_images') 


@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        Category.objects.create(name=category_name, description=description)
        return redirect('admin_panel:manage_categories')
    return redirect('admin_panel:manage_categories')


@login_required
def update_image(request, image_id):
    image = Image.objects.get(id=image_id)
    if request.method == 'POST':
        if 'image_file' in request.FILES:
            image.image_file = request.FILES['image_file']
        image.title = request.POST.get('title', image.title)  # You can add an optional title update
        image.save()
        return redirect('admin_panel:manage_images')
    return redirect('admin_panel:manage_images')  # In case of GET or any issue

@login_required
def delete_image(request, image_id):
    image = Image.objects.get(id=image_id)
    image.delete()
    return redirect('admin_panel:manage_images')

@login_required
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('category_name', category.name)
        category.description = request.POST.get('description', category.description)  # Update description
        category.save()
        return redirect('admin_panel:manage_categories')
    return redirect('admin_panel:manage_categories')

@login_required
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('admin_panel:manage_categories')