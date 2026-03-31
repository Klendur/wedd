from django.contrib import admin
from .models import HousingPreference, TransportInfo, ForumPost, ForumComment, Photo

# ----------------------------
# HousingPreference Admin
# ----------------------------
@admin.register(HousingPreference)
class HousingPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'housing_type', 'guests', 'submitted_at')
    list_filter = ('housing_type', 'submitted_at')
    search_fields = ('user__username', 'name', 'notes')
    ordering = ('-submitted_at',)

# ----------------------------
# TransportInfo Admin
# ----------------------------
@admin.register(TransportInfo)
class TransportInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'arrival_method', 'free_seats', 'coming_from', 'submitted_at')
    list_filter = ('arrival_method', 'submitted_at')
    search_fields = ('user__username', 'name', 'coming_from', 'notes')
    ordering = ('-submitted_at',)

# ----------------------------
# ForumPost Admin
# ----------------------------
@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_at',)

# ----------------------------
# ForumComment Admin
# ----------------------------
@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'content', 'user__username')
    ordering = ('created_at',)

# ----------------------------
# Photo Admin
# ----------------------------
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'uploaded_at')
    search_fields = ('user__username', 'caption')
    ordering = ('-uploaded_at',)