from django.contrib import admin

from .models import Talk, Post, Reply

admin.site.register(Talk)
admin.site.register(Post)
admin.site.register(Reply)