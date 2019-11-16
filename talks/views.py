from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.generic import View, ListView, FormView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
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

    posts_list = Post.objects.values_list('talk__name', 'creator__username', 'content', 'date_created')
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
       
        selected_talk = get_object_or_404(Talk, pk=self.kwargs['talk_pk'])

        context['talk_posts'] = selected_talk.posts.all()

        context['selected_talk'] = selected_talk

        user = self.request.user

        if user.is_authenticated:
            followTalkObj = FollowTalk.objects.filter(user=user, talk=selected_talk)
            
            favoriteTalkObj = FavoriteTalk.objects.filter(user=user, talk=selected_talk)

            if followTalkObj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favoriteTalkObj:
                context['is_favorite'] = True
            else:
                context['is_favorite'] = False

        return context

class PostListView(FormView):
    
    form_class = CommentForm
    template_name = 'post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        user = self.request.user

        context['post'] = post
        context['replies'] = post.replies.all()
        context['talks'] = Talk.objects.all()
      

        if user.is_authenticated:
            followTalkObj = FollowTalk.objects.filter(user=user, talk=post.talk)
            
            favoriteTalkObj = FavoriteTalk.objects.filter(user=user, talk=post.talk)

            if followTalkObj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favoriteTalkObj:
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
            followTalkObj = FollowTalk.objects.filter(user=user, talk=talk)
            
            favoriteTalkObj = FavoriteTalk.objects.filter(user=user, talk=talk)

            if followTalkObj:
                context['userFollows'] = True
            else:
                context['userFollows'] = False

            if favoriteTalkObj:
                context['is_favorite'] = True
            else:
                context['is_favorite'] = False

        context['talk'] = talk

        return context

    def form_valid(self, form):
        talk = Talk.objects.get(pk=self.kwargs['talk_pk'])
        user = self.request.user

        content = form.cleaned_data['content']

        new_post = Post.objects.create(talk=talk, creator=user, content=content)

        return redirect(reverse('talk', kwargs={
            'talk_pk':talk.pk
        }))

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

@login_required(login_url='/auth/login/')
def makeTalkFavorite(request, talk_pk):
    """This functions view receives a request with the talk's pk and enables logged in users to make a talk a favorite."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    
    if current_user.is_authenticated:
        userObj = User.objects.get(pk=current_user.id)
        talkObj = Talk.objects.get(pk=talk_pk)

        favoriteTalkObj = FavoriteTalk.objects.filter(user = userObj, talk = talkObj)

        if favoriteTalkObj:
            favoriteTalkObj.delete()
            

        else:
            favoriteTalkObj = FavoriteTalk.objects.create(user=userObj, talk = talkObj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def likePost(request, post_pk):
    """This functions view receives a request with the post's pk and enables logged in users to like or unlike a post."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        userObj = User.objects.get(pk=current_user.id)
        postObj = Post.objects.get(pk=post_pk)

        likePostObj = LikePost.objects.filter(user = userObj, post = postObj)

        if likePostObj:
            likePostObj.delete()
            

        else:
            likePostObj = LikePost.objects.create(user=userObj, post = postObj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def likeReply(request, reply_pk):
    """This functions view receives a request with the reply's pk and enables logged in users to like or unlike a reply."""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        userObj = User.objects.get(pk=current_user.id)
        replyObj = Reply.objects.get(pk=reply_pk)

        likeReplyObj = LikeReply.objects.filter(user = userObj, reply = replyObj)

        if likeReplyObj:
            likeReplyObj.delete()
            

        else:
            likeReplyObj = LikeReply.objects.create(user=userObj, reply = replyObj)

        return redirect(url)

    else:
        return redirect(reverse('signIn'))

def deleteReply(request, reply_pk):
    """This function gets a request with a reply pk as a parameter and we use it to delete a reply"""

    url = request.META.get('HTTP_REFERER')
    current_user = request.user

    if current_user.is_authenticated:
        replyObj = Reply.objects.filter(creator=current_user, pk=reply_pk)

        if replyObj:
            replyObj.delete()
        
        return redirect(url)

def searchBarRedirect(request):
    talk_name = request.GET.get('talk-name-input')
    talkObj = get_object_or_404( Talk,name__icontains=talk_name)
    
    return redirect(reverse('talk', kwargs={'talk_pk':talkObj.pk}))
