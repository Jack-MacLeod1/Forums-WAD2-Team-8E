from django.contrib import admin
from forum_app.models import Category, Post, Comment, UserProfile

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)