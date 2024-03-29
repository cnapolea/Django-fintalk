from django.urls import path

from .views.views import IndexListView, TalkListView, PostListView, CreatePostFormView, UserProfile

from .views.talks_ajax_requests_functions import talk_request, get_page
from .views.buttons_functionality import follow_talk_manager, like_post, like_reply, delete_reply, make_talk_favorite, search_bar_redirect, delete_post, follow_user

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('talk/<int:talk_pk>/', TalkListView.as_view(), name = 'talk'),
    path('talk/<int:talk_pk>/create_post/', CreatePostFormView.as_view(), name = 'create_post'),
    path('talk/<int:talk_pk>/post/<int:post_pk>/', PostListView.as_view(), name = 'post_view'),
    path('profile/<str:username>/', UserProfile.as_view(), name='user_profile'),
    path('profile/follow_user/<int:user_pk>/', follow_user, name='follow_user'),
    path('talk/post/like_reply/<int:reply_pk>', like_reply, name = 'like_reply'),
    path('talk/post/delete_reply/<int:reply_pk>', delete_reply, name = 'delete_reply'),
    path('talk/post/delete_post/<int:post_pk>', delete_post, name = 'delete_post'),
    path('talk/follow_talk/<int:talk_pk>/', follow_talk_manager, name = 'followTalk'),
    path('talk/favorite_talk/<int:talk_pk>/', make_talk_favorite, name = 'make_favorite'),
    path('post/like_post/<int:post_pk>/', like_post, name = 'like_post'),
    path('ajax/talk_request/', talk_request, name = 'talk_request'),
    path('ajax/page_request/', get_page, name = 'get_page'),
    path('talk/get/', search_bar_redirect, name = 'get_talk'),
]