from django.views.generic import View, ListView, FormView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from .models import Talk, FollowTalk, Topic, Post, LikePost, UserFollowUser

class IndexListView(ListView):
    """Homepage view. This will receive a list of talk (most populars) 
    which will be displayed to users"""

    model = Topic
    context_object_name = 'topics'
    template_name = 'index.html'
    
    # def get_queryset(self):
    #     self.talks = get_object_or_404(Talk)
    #     queryset = self.talks
    #     return queryset