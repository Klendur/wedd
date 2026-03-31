# website/models.py

from django.db import models
from django.contrib.auth.models import User


class HousingPreference(models.Model):
    HOUSING_CHOICES = [
        ('peamaja', 'Peamaja'),
        ('camping', 'Camping'),
        ('eraldi', 'Eraldi majutus (+60€)'),
        ('ei_jaa', 'Ei jää ööseks'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='housing_preferences')
    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.get_housing_type_display()}"


class TransportInfo(models.Model):
    ARRIVAL_CHOICES = [
        ('own_car', 'Oma autoga / Own car'),
        ('bus', 'Bussiga / Bus'),
        ('taxi', 'Takso/Bolt'),
        ('with_someone', 'Sõidan kaasa / Getting a ride'),
        ('other', 'Muu / Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_info')
    arrival_method = models.CharField(max_length=20, choices=ARRIVAL_CHOICES)
    free_seats = models.PositiveIntegerField(default=0)
    coming_from = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.get_arrival_method_display()}"


class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class PhotoGallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Galerii: {self.user.username} ({self.uploaded_at.strftime('%d.%m.%Y')})"


class Photo(models.Model):
    gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name='photos')
    image = models.FileField(upload_to='photos/')  # allow videos too
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def is_video(self):
        return self.image.name.lower().endswith(('.mp4', '.mov', '.webm'))

    def is_image(self):
        return self.image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))