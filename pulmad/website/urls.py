from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('majutus/', views.housing, name='housing'),
    path('toit/', views.food, name='food'),
    path('info/', views.info, name='info'),
    path('transport/', views.transport, name='transport'),
    path('foorum/', views.forum, name='forum'),
    path('foorum/kommentaar/<int:post_id>/', views.forum_comment, name='forum_comment'),
    path('foorum/kustuta/<int:post_id>/', views.forum_delete_post, name='forum_delete_post'),
    path('fotod/', views.photos, name='photos'),
    path('fotod/kustuta/<int:photo_id>/', views.delete_photo, name='delete_photo'),
]
