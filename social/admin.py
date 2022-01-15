from django.contrib import admin
from .models import Post, Files, UserProfile


admin.site.register(Post)
admin.site.register(Files)
admin.site.register(UserProfile)
