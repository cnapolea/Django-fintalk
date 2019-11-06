from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import View, ListView, FormView, UpdateView
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.utils import timezone
from django.urls import reverse


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
    """This gets the list of objects of the next page. Assists in the pagination on scroll"""
    topics_list = Topic.objects.values_list('talk__name', 'creator__username', 'description', 'date_created', 'views')
    paginator = Paginator(topics_list, 4)

    page_num = request.GET.get('page')
    
    try:
        page = paginator.page(page_num)
        context = {'topics':list(page.object_list)}
    except:
        context = {'topics': None}
    return JsonResponse(context)

class TalkListView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        selected_talk = get_object_or_404(Talk, pk=self.kwargs['talk_pk'])

        context['talk_topics'] = selected_talk.topics.all()

        context['selected_talk'] = selected_talk

        user = self.request.user

        if user.is_authenticated:
            followTalkObj = FollowTalk.objects.filter(user=user, talk=selected_talk)

            if followTalkObj:
                context['userFollows'] = True

            else:
                context['userFollows'] = False

        return context

@login_required(login_url='/auth/login/')
def followTalkManager(request, talk_pk):
    """This functions view receives a request to with the talk's pk and enables logged in users to follow or unfollow a talk."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    
    if current_user.is_authenticated:
        userObj = User.objects.get(pk=current_user.id)
        talkObj = Talk.objects.get(pk=talk_pk)

        followTalkObj = FollowTalk.objects.filter(user = userObj, talk = talkObj)

        if followTalkObj:
            followTalkObj.delete()
            

        else:
            followTalkObj = FollowTalk.objects.create(user=userObj, talk = talkObj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))