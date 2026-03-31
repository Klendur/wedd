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
    name = models.CharField(max_length=200)
    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES)
    guests = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.get_housing_type_display()}"


class TransportInfo(models.Model):
    ARRIVAL_CHOICES = [
        ('own_car', 'Oma autoga'),
        ('bus', 'Bussiga'),
        ('taxi', 'Takso/Bolt'),
        ('with_someone', 'Sõidan kaasa'),
        ('other', 'Muu'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_info')
    name = models.CharField(max_length=200)
    arrival_method = models.CharField(max_length=20, choices=ARRIVAL_CHOICES)
    free_seats = models.PositiveIntegerField(default=0, help_text='Vabad kohad autos (0 kui ei sõida autoga)')
    coming_from = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.get_arrival_method_display()}"


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

    def __str__(self):
        return f"Kommentaar: {self.post.title} poolt {self.user.username}"


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Foto: {self.user.username} ({self.uploaded_at.strftime('%d.%m.%Y')})"
