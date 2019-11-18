from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse

from ..models import Talk, Post, Reply, FollowTalk, FavoriteTalk, LikePost, LikeReply

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
