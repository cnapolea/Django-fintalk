from django.urls import path

from .views import IndexListView, TalkListView,talkRequest, get_page, followTalkManager, PostListView, likePost, likeReply, deleteReply, makeTalkFavorite

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('talk/<int:talk_pk>/', TalkListView.as_view(), name = 'talk'),
    path('talk/<int:talk_pk>/post/<int:post_pk>/', PostListView.as_view(), name = 'post_view'),
    path('talk/post/like_reply/<int:reply_pk>', likeReply, name = 'like_reply'),
    path('talk/post/delete_reply/<int:reply_pk>', deleteReply, name = 'delete_reply'),
    path('talk/follow_talk/<int:talk_pk>/', followTalkManager, name = 'followTalk'),
    path('talk/favorite_talk/<int:talk_pk>/', makeTalkFavorite, name = 'makeFavorite'),
    path('post/like_post/<int:post_pk>/', likePost, name = 'like_post'),
    path('ajax/talk_request/', talkRequest, name = 'talk_request'),
    path('ajax/page_request/', get_page, name = 'get_page'),
]