from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from accounts.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='social/profile-pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=256, null=True)
    like_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.like_by.count()

    def like_status(self, user):
        if user.is_authenticated:
            return self.like_by.filter(id=user.id).exists()
        return False

class Follow(models.Model):
    
    # user who is following
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    # user who is being followed
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # prevent duplicate follow relationships
        unique_together = ('following', 'follower')
