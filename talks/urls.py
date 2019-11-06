from django.urls import path

from .views import IndexListView, TalkListView,talkRequest, get_page, followTalkManager

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('talk/<int:talk_pk>/', TalkListView.as_view(), name = 'talk'),
    path('talk/follow_talk/<int:talk_pk>/', followTalkManager, name = 'followTalk'),
    path('ajax/talk_request/', talkRequest, name = 'talk_request'),
    path('ajax/page_request/', get_page, name = 'get_page'),
]