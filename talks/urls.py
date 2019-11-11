from django.urls import path

from .views import IndexListView, TalkListView,talkRequest, get_page, followTalkManager, PostListView, likePost

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('talk/<int:talk_pk>/', TalkListView.as_view(), name = 'talk'),
    path('talk/<int:talk_pk>/post/<int:post_pk>/', PostListView.as_view(), name = 'post_view'),
    path('talk/follow_talk/<int:talk_pk>/', followTalkManager, name = 'followTalk'),
    path('post/like_post/<int:post_pk>/', likePost, name = 'like_post'),
    path('ajax/talk_request/', talkRequest, name = 'talk_request'),
    path('ajax/page_request/', get_page, name = 'get_page'),
]