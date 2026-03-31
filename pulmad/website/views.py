from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import HousingPreference, TransportInfo, ForumPost, ForumComment, Photo
from .forms import HousingForm, TransportForm, ForumPostForm, ForumCommentForm, PhotoUploadForm


# ── Auth ────────────────────────────────────────────────────────────────────

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
        messages.error(request, _('Vale kasutajanimi või parool.'))
    return render(request, 'website/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Main pages ───────────────────────────────────────────────────────────────

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
            messages.success(request, _('Majutuseelistus salvestatud!'))
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
            messages.success(request, _('Transpordiinfo salvestatud!'))
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
            messages.success(request, _('Postitus lisatud!'))
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
            messages.success(request, _('Kommentaar lisatud!'))
    return redirect('forum')


@login_required
def forum_delete_post(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, _('Postitus kustutatud.'))
    return redirect('forum')


@login_required
def photos(request):
    all_photos = Photo.objects.select_related('user').all()
    form = PhotoUploadForm()

    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, _('Foto üles laaditud!'))
            return redirect('photos')

    return render(request, 'website/photos.html', {
        'photos': all_photos,
        'form': form,
    })


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, user=request.user)
    if request.method == 'POST':
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, _('Foto kustutatud.'))
    return redirect('photos')
