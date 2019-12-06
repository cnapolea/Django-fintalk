from django.views.generic import ListView, FormView, TemplateView
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from ..models import Talk, FollowTalk, Post, Reply, LikePost, LikeReply, UserFollowUser, FavoriteTalk
from ..forms import CommentForm, PostForm

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

class TalkListView(ListView):
    model = Talk
    template_name = 'talk.html'
    context_object_name = 'talks'    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        selected_talk = Talk.objects.prefetch_related('posts').get(pk=self.kwargs['talk_pk'])

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
        post = Post.objects.prefetch_related('replies').get(pk=self.kwargs['post_pk'])
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
        
@method_decorator(login_required(login_url='/auth/login/'), name = 'dispatch')
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

class UserProfile(TemplateView):
    """This view handles the display of the user's profile"""

    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        talks = Talk.objects.all()

        profile_owner = self.request.user.follows.filter(being_followed=user)

        if profile_owner.count() >= 1:
            context['being_followed'] = True
        else:
            context['being_followed'] = False

        context['user'] = user
        context['talks'] = talks 

        return context
