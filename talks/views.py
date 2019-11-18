from django.views.generic import View, ListView, FormView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse


from .models import Talk, FollowTalk, Post, Reply, LikePost, LikeReply, UserFollowUser, FavoriteTalk
from .forms import CommentForm, PostForm

class IndexListView(ListView):
    """Homepage view. This will receive a list of talk (most populars) 
    which will be displayed to users"""

    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'
    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['talks'] = Talk.objects.all()
        context['follow_talks'] = FollowTalk.objects.all()
        return context
    
def talk_request(request):
    """Takes a user request to find a talk and it returns a json object
    with talk names if the match exists or it returns None as json object"""

    user_input = request.GET.get('talk-name-input')
    if not user_input:
        data = {'matchedTalks': None}
        return JsonResponse(data)
    else:     
        talks = Talk.objects.filter(
                    name__icontains=f'{user_input}').values_list('name', flat=True)
        if talks:        
            data = {'matchedTalks': list(talks)}
            return JsonResponse(data)
        
        else:
            data = {'matchedTalks': 'No results found'}
            return JsonResponse(data)

def get_page(request):
    """This gets the list of objects of the next page. Assists in the pagination on scroll"""

    posts_list = Post.objects.values_list(
                    'talk__name', 'creator__username', 
                    'content', 'date_created')
    paginator = Paginator(posts_list, 4)

    page_num = request.GET.get('page')
    
    try:
        page = paginator.page(page_num)
        context = {'posts':list(page.object_list)}
    except:
        context = {'posts': None}
    return JsonResponse(context)

class TalkListView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        selected_talk = Talk.objects.select_related('posts').get(pk=self.kwargs['talk_pk'])

        context['talk_posts'] = selected_talk.posts.all()

        context['selected_talk'] = selected_talk

        user = self.request.user

        if user.is_authenticated:
            follow_talk_obj = FollowTalk.objects.filter(user=user, talk=selected_talk)
            
            favorite_talk_obj = FavoriteTalk.objects.filter(user=user, talk=selected_talk)

            if follow_talk_obj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favorite_talk_obj:
                context['is_favorite'] = True
            else:
                context['is_favorite'] = False

        return context

class PostListView(FormView):
    
    form_class = CommentForm
    template_name = 'post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.select_related('replies').get(pk=self.kwargs['post_pk'])
        user = self.request.user

        context['post'] = post
        context['replies'] = post.replies.all()
        context['talks'] = Talk.objects.all()
      

        if user.is_authenticated:
            follow_talk_obj = FollowTalk.objects.filter(user=user, talk=post.talk)
            
            favorite_talk_obj = FavoriteTalk.objects.filter(user=user, talk=post.talk)

            if follow_talk_obj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favorite_talk_obj:
                context['is_favorite'] = True
            else:
                context['is_favorite'] = False

        return context
    
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        user = self.request.user
        reply = form.cleaned_data['reply']
        new_reply = Reply.objects.create(post=post, creator=user, reply=reply)

        return redirect(self.request.META.get('HTTP_REFERER'))    

class CreatePostFormView(FormView):
    form_class = PostForm
    template_name = 'create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        talk = get_object_or_404(Talk, pk=self.kwargs['talk_pk'])
        user = self.request.user
        

        if user.is_authenticated:
            follow_talk_obj = FollowTalk.objects.filter(user=user, talk=talk)
            
            favorite_talk_obj = FavoriteTalk.objects.filter(user=user, talk=talk)

            if follow_talk_obj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favorite_talk_obj:
                context['is_favorite'] = True
            else:
                context['is_favorite'] = False

        context['talk'] = talk

        return context

    def form_valid(self, form):
        talk = Talk.objects.get(pk=self.kwargs['talk_pk'])
        user = self.request.user

        content = form.cleaned_data['content']

        new_post = Post.objects.create(
                    talk=talk, creator=user, 
                    content=content)

        return redirect(reverse('talk', kwargs={'talk_pk':talk.pk} ))

@login_required(login_url='/auth/login/')
def follow_talk_manager(request, talk_pk):
    """This functions view receives a request to with the talk's pk and enables logged in users to follow or unfollow a talk."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    
    if current_user.is_authenticated:
        talk_obj = Talk.objects.get(pk=talk_pk)

        follow_talk_obj = FollowTalk.objects.filter(user = current_user, talk = talk_obj)

        if follow_talk_obj:
            follow_talk_obj.delete()
            

        else:
            follow_talk_obj = FollowTalk.objects.create(user=current_user, talk = talk_obj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def make_talk_favorite(request, talk_pk):
    """This functions view receives a request with the talk's pk and enables logged in users to make a talk a favorite."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    
    if current_user.is_authenticated:
        talk_obj = Talk.objects.get(pk=talk_pk)

        favorite_talk_obj = FavoriteTalk.objects.filter(user = current_user, talk = talk_obj)

        if favorite_talk_obj:
            favorite_talk_obj.delete()
            

        else:
            favorite_talk_obj = FavoriteTalk.objects.create(user = current_user, talk = talk_obj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def like_post(request, post_pk):
    """This functions view receives a request with the post's pk and enables logged in users to like or unlike a post."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        post_obj = Post.objects.get(pk=post_pk)

        like_post_obj = LikePost.objects.filter(user = current_user, post = post_obj)

        if like_post_obj:
            like_post_obj.delete()
            

        else:
            like_post_obj = LikePost.objects.create(user=current_user, post = post_obj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def like_reply(request, reply_pk):
    """This functions view receives a request with the reply's pk and enables logged in users to like or unlike a reply."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        reply_obj = Reply.objects.get(pk=reply_pk)

        like_reply_obj = LikeReply.objects.filter(user = current_user, reply = reply_obj)

        if like_reply_obj:
            like_reply_obj.delete()
            

        else:
            like_reply_obj = LikeReply.objects.create(user=current_user, reply = reply_obj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

def delete_reply(request, reply_pk):
    """This function gets a request with a reply pk as a parameter and we use it to delete a reply"""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        reply_obj = Reply.objects.filter(creator=current_user, pk=reply_pk)

        if reply_obj:
            reply_obj.delete()
        
        return redirect(url)

def delete_post(request, post_pk):
    """This function gets a request with a post pk as a parameter and we use it to delete a post"""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        post_obj = Post.objects.filter(creator=current_user, pk=post_pk)

        if post_obj:
            post_obj.delete()
        
        return redirect(url)

def search_bar_redirect(request):
    talk_name = request.GET.get('talk-name-input')
    talk_obj = Talk.objects.filter(name__icontains=talk_name)
    
    return redirect(reverse('talk', kwargs={'talk_pk':talk_obj.pk}))
