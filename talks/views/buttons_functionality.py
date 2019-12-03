from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User

from ..models import Talk, Post, Reply, FollowTalk, UserFollowUser, FavoriteTalk, LikePost, LikeReply

def create_or_delete_middle_table_obj(related_db_object, middle_table_object, user, pk, **kwargs):
    current_user = user 
    related_db_obj = related_db_object
    middle_table_obj = middle_table_object

    if current_user.is_authenticated:
        model_obj = related_db_obj.objects.get(pk=pk)
        
        if kwargs['column_name_1'] == 'talk':

            link_obj = middle_table_obj.objects.filter(user = current_user, talk = model_obj)

            if link_obj:
                link_obj.delete()

            else:
                middle_table_obj.objects.create(user=current_user, talk = model_obj)
            

        elif kwargs['column_name_1'] == 'post':

            link_obj = middle_table_obj.objects.filter(user = current_user, post = model_obj)

            if link_obj:
                link_obj.delete()
            
            else:
                middle_table_obj.objects.create(user=current_user, post = model_obj)
        
        
        elif kwargs['column_name_1'] == 'reply':

            link_obj = middle_table_obj.objects.filter(user=current_user, reply = model_obj)

            if link_obj:
                link_obj.delete()

            else:
                middle_table_obj.objects.create(user=current_user, reply = model_obj)
        
        elif kwargs['column_name_1'] == 'follower' and kwargs['column_name_2'] == 'being_followed':

            link_obj = middle_table_obj.objects.filter(follower=current_user, being_followed = model_obj)

            if link_obj:
                link_obj.delete()
            
            else:
                middle_table_obj.objects.create(follower=current_user, being_followed = model_obj)
            
        return True

    else:
        return False

def delete_reply_or_post_obj(related_db_obj, user, pk):
    current_user = user

    if current_user.is_authenticated:
        model_obj = related_db_obj.objects.filter(creator=current_user, pk=pk)

        if model_obj:
            model_obj.delete()
        
        return True

@login_required(login_url='/auth/login/')
def follow_talk_manager(request, talk_pk):
    """This functions view receives a request to with the talk's pk and enables logged in users to follow or unfollow a talk."""

    url = request.META.get('HTTP_REFERER')
    if create_or_delete_middle_table_obj(Talk, FollowTalk, 
                                      request.user, talk_pk, column_name_1='talk'):
                                      return redirect(url)
    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def make_talk_favorite(request, talk_pk):
    """This functions view receives a request with the talk's pk and enables logged in users to make a talk a favorite."""

    url = request.META.get('HTTP_REFERER')
    if create_or_delete_middle_table_obj(Talk, FavoriteTalk, 
                                      request.user, talk_pk, column_name_1='talk'):
                                      return redirect(url)
    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def like_post(request, post_pk):
    """This functions view receives a request with the post's pk and enables logged in users to like or unlike a post."""

    url = request.META.get('HTTP_REFERER')
    if create_or_delete_middle_table_obj(Post, LikePost, 
                                      request.user, post_pk, column_name_1='post'):
                                      return redirect(url)
    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def follow_user(request, user_pk):
    """This functions view receives a request with the user's pk and enables logged in users to follow or unfollow another user."""

    url = request.META.get('HTTP_REFERER')
    if create_or_delete_middle_table_obj(User, UserFollowUser, 
                                      request.user, user_pk, column_name_1='follower', column_name_2='being_followed'):
                                      return redirect(url)
    else:
        return redirect(reverse('signIn'))

@login_required(login_url='/auth/login/')
def like_reply(request, reply_pk):
    """This functions view receives a request with the reply's pk and enables logged in users to like or unlike a reply."""

    url = request.META.get('HTTP_REFERER')
    if create_or_delete_middle_table_obj(Reply, LikeReply, 
                                      request.user, reply_pk, column_name_1='reply'):
                                      return redirect(url)
    else:
        return redirect(reverse('signIn'))

def delete_reply(request, reply_pk):
    """This function gets a request with a reply pk as a parameter and we use it to delete a reply"""

    url = request.META.get('HTTP_REFERER')
    
    if delete_reply_or_post_obj(Reply, request.user, reply_pk):
        return redirect(url) 
    
def delete_post(request, post_pk):
    """This function gets a request with a post pk as a parameter and we use it to delete a post"""

    url = request.META.get('HTTP_REFERER')
    if delete_reply_or_post_obj(Post, request.user, post_pk):
        return redirect(url)

def search_bar_redirect(request):
    talk_name = request.GET.get('talk-name-input')
    talk_obj = Talk.objects.get(name__icontains=talk_name)
    
    return redirect(reverse('talk', kwargs={'talk_pk':talk_obj.pk}))
