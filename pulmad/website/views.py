# website/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import HousingPreference, TransportInfo, ForumPost, ForumComment, Photo, PhotoGallery, RSVP
from .forms import HousingForm, TransportForm, ForumPostForm, ForumCommentForm, PhotoUploadForm
import io
import zipfile
from django.http import HttpResponse, Http404

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# -----------------------------
# PIN login system
# -----------------------------
VALID_PINS = ["888444"]  # Replace with your actual PINs

def pin_login(request):
    """Log in using a PIN only"""
    if request.session.get('has_access'):
        return redirect('home')
    if request.method == 'POST':
        pin = request.POST.get('pin')
        if pin in VALID_PINS:
            request.session['has_access'] = True
            return redirect('home')
        messages.error(request, "Invalid PIN")
    return render(request, 'website/login.html')


def pin_logout(request):
    """Log out"""
    request.session.flush()
    return redirect('login')


def pin_required(view_func):
    """Decorator to enforce PIN login"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('has_access'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# -----------------------------
# Language selector
# -----------------------------
def set_lang(request):
    lang = request.POST.get('lang', 'et')
    if lang in ('et', 'en'):
        request.session['lang'] = lang
    return redirect(request.POST.get('next', '/'))

# -----------------------------
# Home & RSVP
# -----------------------------
# views.py
@pin_required
def home(request):
    rsvp = RSVP.objects.filter(session_key=request.session.session_key).first()
    return render(request, 'website/home.html', {'rsvp': rsvp})


@pin_required
def toggle_rsvp(request):
    if request.method == 'POST':
        name = request.POST.get('user', '').strip()
        if not name:
            messages.error(request, "Please enter your name.")
            return redirect('home')

        # Save RSVP for this session
        RSVP.objects.create(user=name, coming=True)

        messages.success(request, "Successfully signed up!")
    return redirect('home')

# -----------------------------
# Housing
# -----------------------------
@pin_required
def housing(request):
    submission = None
    form = HousingForm(request.POST or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Majutuseelistus salvestatud! / Accommodation saved!')
        return redirect('housing')
    return render(request, 'website/housing.html', {'form': form, 'submission': submission})

# -----------------------------
# Transport
# -----------------------------
@pin_required
def transport(request):
    submission = None
    form = TransportForm(request.POST or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Transpordiinfo salvestatud! / Transport info saved!')
        return redirect('transport')

    drivers = TransportInfo.objects.filter(arrival_method='own_car', free_seats__gt=0)
    return render(request, 'website/transport.html', {'form': form, 'submission': submission, 'drivers': drivers})

# -----------------------------
# Forum
# -----------------------------
@pin_required
def forum(request):
    posts = ForumPost.objects.prefetch_related('comments').all()
    form = ForumPostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Postitus lisatud! / Post added!')
        return redirect('forum')
    return render(request, 'website/forum.html', {'posts': posts, 'form': form, 'comment_form': ForumCommentForm()})

@pin_required
def forum_comment(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    form = ForumCommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, 'Kommentaar lisatud! / Comment added!')
    return redirect('forum')

@pin_required
def forum_delete_post(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Postitus kustutatud. / Post deleted.')
    return redirect('forum')

# -----------------------------
# Photos
# -----------------------------
@pin_required
def photos(request):
    galleries = PhotoGallery.objects.prefetch_related('photos').all()
    return render(request, 'website/photos.html', {'galleries': galleries})

@pin_required
def photos_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        caption = request.POST.get('caption', '')

        if not files:
            messages.error(request, "No files selected.")
            return redirect('photos')

        for f in files:
            if f.size > MAX_FILE_SIZE:
                messages.error(request, f"{f.name} is too large (max 100MB)")
                return redirect('photos')

        gallery = PhotoGallery.objects.create(caption=caption)
        for f in files:
            Photo.objects.create(gallery=gallery, image=f)

        messages.success(request, "Files uploaded successfully!")
        return redirect('photos')

    galleries = PhotoGallery.objects.prefetch_related('photos').all()
    return render(request, 'website/photos.html', {'galleries': galleries})

@pin_required
def delete_gallery(request, gallery_id):
    gallery = get_object_or_404(PhotoGallery, pk=gallery_id)
    if request.method == 'POST':
        for photo in gallery.photos.all():
            photo.image.delete(save=False)
        gallery.delete()
        messages.success(request, 'Galerii kustutatud. / Gallery deleted.')
    return redirect('photos')

@pin_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.method == 'POST':
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, 'Foto kustutatud. / Photo deleted.')
    return redirect('photos')

@pin_required
def download_gallery(request, gallery_id):
    gallery = get_object_or_404(PhotoGallery, pk=gallery_id)
    photos = gallery.photos.all()
    if not photos.exists():
        raise Http404("No files to download in this gallery.")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for photo in photos:
            if photo.image:
                filename = photo.image.name.split('/')[-1]
                zip_file.writestr(filename, photo.image.read())
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=gallery_{gallery.id}.zip'
    return response

# -----------------------------
# Static Pages
# -----------------------------
@pin_required
def food(request):
    return render(request, 'website/food.html')

@pin_required
def info(request):
    return render(request, 'website/info.html')

@pin_required
def games(request):
    return render(request, 'website/games.html')