# website/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import HousingPreference, TransportInfo, ForumPost, ForumComment, Photo
from .forms import HousingForm, TransportForm, ForumPostForm, ForumCommentForm, PhotoUploadForm


def set_lang(request):
    lang = request.POST.get('lang', 'et')
    if lang in ('et', 'en'):
        request.session['lang'] = lang
    return redirect(request.POST.get('next', '/'))


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Vale kasutajanimi või parool. / Incorrect username or password.')
    return render(request, 'website/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'website/home.html')


@login_required
def housing(request):
    user_submission = HousingPreference.objects.filter(user=request.user).first()
    form = HousingForm(instance=user_submission)
    if request.method == 'POST':
        form = HousingForm(request.POST, instance=user_submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Majutuseelistus salvestatud! / Accommodation saved!')
            return redirect('housing')
    return render(request, 'website/housing.html', {
        'form': form,
        'submission': user_submission,
    })


@login_required
def food(request):
    return render(request, 'website/food.html')


@login_required
def info(request):
    return render(request, 'website/info.html')


@login_required
def transport(request):
    user_submission = TransportInfo.objects.filter(user=request.user).first()
    form = TransportForm(instance=user_submission)
    if request.method == 'POST':
        form = TransportForm(request.POST, instance=user_submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Transpordiinfo salvestatud! / Transport info saved!')
            return redirect('transport')
    all_drivers = TransportInfo.objects.filter(
        arrival_method='own_car', free_seats__gt=0
    ).exclude(user=request.user)
    return render(request, 'website/transport.html', {
        'form': form,
        'submission': user_submission,
        'drivers': all_drivers,
    })


@login_required
def forum(request):
    posts = ForumPost.objects.select_related('user').prefetch_related('comments__user').all()
    form = ForumPostForm()
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Postitus lisatud! / Post added!')
            return redirect('forum')
    return render(request, 'website/forum.html', {
        'posts': posts,
        'form': form,
        'comment_form': ForumCommentForm(),
    })


@login_required
def forum_comment(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Kommentaar lisatud! / Comment added!')
    return redirect('forum')


@login_required
def forum_delete_post(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postitus kustutatud. / Post deleted.')
    return redirect('forum')


@login_required
def photos(request):
    from .models import PhotoGallery
    galleries = PhotoGallery.objects.select_related('user').prefetch_related('photos').all()
    return render(request, 'website/photos.html', {'galleries': galleries})


@login_required
def photos_upload(request):
    from .models import PhotoGallery, Photo
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        caption = request.POST.get('caption', '')
        if files:
            gallery = PhotoGallery.objects.create(user=request.user, caption=caption)
            for f in files:
                Photo.objects.create(gallery=gallery, image=f)
            messages.success(request, 'Fotod üles laaditud! / Photos uploaded!')
    return redirect('photos')


@login_required
def delete_gallery(request, gallery_id):
    from .models import PhotoGallery
    gallery = get_object_or_404(PhotoGallery, pk=gallery_id, user=request.user)
    if request.method == 'POST':
        for photo in gallery.photos.all():
            photo.image.delete(save=False)
        gallery.delete()
        messages.success(request, 'Galerii kustutatud. / Gallery deleted.')
    return redirect('photos')


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, gallery__user=request.user)
    if request.method == 'POST':
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, 'Foto kustutatud. / Photo deleted.')
    return redirect('photos')


@login_required
def games(request):
    return render(request, 'website/games.html')