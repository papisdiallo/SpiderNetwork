from django.contrib import admin
from .models import Post, Files, UserProfile, Comment


admin.site.register(Post)
admin.site.register(Files)
admin.site.register(Comment)
admin.site.register(UserProfile)
