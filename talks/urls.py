from django.urls import path

from .views import IndexListView, talkRequest

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('ajax/talk_request/', talkRequest, name = 'talk_request'),
]