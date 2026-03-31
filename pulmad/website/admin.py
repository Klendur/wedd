from django.contrib import admin
from .models import (
    HousingPreference,
    TransportInfo,
    ForumPost,
    ForumComment,
    PhotoGallery,
    Photo
)


# ------------------------
# Housing
# ------------------------
@admin.register(HousingPreference)
class HousingPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'housing_type', 'guests', 'submitted_at')
    list_filter = ('housing_type', 'submitted_at')
    search_fields = ('user__username', 'notes')
    ordering = ('-submitted_at',)


# ------------------------
# Transport
# ------------------------
@admin.register(TransportInfo)
class TransportInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'arrival_method', 'free_seats', 'coming_from', 'submitted_at')
    list_filter = ('arrival_method', 'submitted_at')
    search_fields = ('user__username', 'coming_from', 'notes')
    ordering = ('-submitted_at',)


# ------------------------
# Forum Comments Inline
# ------------------------
class ForumCommentInline(admin.TabularInline):
    model = ForumComment
    extra = 0
    readonly_fields = ('user', 'content', 'created_at')
    can_delete = True


# ------------------------
# Forum Posts
# ------------------------
@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [ForumCommentInline]


# ------------------------
# Forum Comments (standalone)
# ------------------------
@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'post__title')
    list_filter = ('created_at',)
    ordering = ('created_at',)


# ------------------------
# Photos Inline
# ------------------------
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


# ------------------------
# Photo Galleries
# ------------------------
@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'uploaded_at')
    search_fields = ('user__username', 'caption')
    ordering = ('-uploaded_at',)
    inlines = [PhotoInline]


# ------------------------
# Photos (standalone)
# ------------------------
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'uploaded_at')
    list_filter = ('uploaded_at',)
    ordering = ('uploaded_at',)