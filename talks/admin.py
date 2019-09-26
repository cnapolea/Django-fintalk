from django.contrib import admin

from .models import Talk, FollowTalk, Topic, Post, LikePost, UserFollowUser

admin.site.register(Talk)
admin.site.register(Topic)
admin.site.register(Post)