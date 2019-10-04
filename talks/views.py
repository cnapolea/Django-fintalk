from django.views.generic import View, ListView, FormView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse

from .models import Talk, FollowTalk, Topic, Post, LikePost, UserFollowUser

class IndexListView(ListView):
    """Homepage view. This will receive a list of talk (most populars) 
    which will be displayed to users"""

    model = Topic
    context_object_name = 'topics'
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talks'] = Talk.objects.all()[:3]
        context['follow_talks'] = FollowTalk.objects.all()
        return context

def talkRequest(request):
    """Takes a user request to find a talk and it returns a json object
    with talk names if the match exists or it returns None as json object"""

    user_input = request.GET.get('talk-name-input', None)
    if not user_input:
        data = {'Matched Talks': None}
        return JsonResponse(data)
    else:     
        talks = Talk.objects.filter(name__istartswith=f'{user_input}')
        
        if talks:
            talk_names = [x.name for x in talks]
            
            if len(talk_names) >= 6:
                data = {'Matched Talks': talk_names[:6]}
            else:
                data = {'Matched Talks': talk_names}

            return JsonResponse(data)
        
        else:
            data = {'Matched Talks': f'No talk starts with {user_input}'}
            return JsonResponse(data)