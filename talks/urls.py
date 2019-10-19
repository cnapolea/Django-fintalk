from django.urls import path

from .views import IndexListView, talkRequest, get_page

urlpatterns = [
    path('', IndexListView.as_view(), name = 'homepage'),
    path('ajax/talk_request/', talkRequest, name = 'talk_request'),
    path('ajax/page_request/', get_page, name = 'get_page'),
]