from django.http import HttpResponse, HttpRequest
from django.views.generic import View, ListView, FormView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
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
    paginate_by = 4
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talks'] = Talk.objects.all()
        context['follow_talks'] = FollowTalk.objects.all()
        return context
    


def talkRequest(request):
    """Takes a user request to find a talk and it returns a json object
    with talk names if the match exists or it returns None as json object"""

    user_input = request.GET.get('talk-name-input')
    if not user_input:
        data = {'matchedTalks': None}
        return JsonResponse(data)
    else:     
        talks = Talk.objects.filter(name__icontains=f'{user_input}').values_list('name', flat=True)
        if talks:        
            data = {'matchedTalks': list(talks)}
            return JsonResponse(data)
        
        else:
            data = {'matchedTalks': 'No results found'}
            return JsonResponse(data)

def get_page(request):
    
    topics_list = Topic.objects.values_list('talk__name', 'creator__username', 'description', 'date_created', 'views')
    paginator = Paginator(topics_list, 4)

    page_num = request.GET.get('page')
    
    try:
        page = paginator.page(page_num)
        context = {'topics':list(page.object_list)}
    except:
        context = {'topics': None}
    return JsonResponse(context)
