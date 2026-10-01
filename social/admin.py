from django.contrib import admin

# Register your models here.
from .models import Post, Follow, Profile

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Profile)

admin.site.site_header = "Social Network Admin"
