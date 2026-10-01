
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
