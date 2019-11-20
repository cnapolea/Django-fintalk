from django.http import JsonResponse
from django.core.paginator import Paginator

from ..models import Talk, Post

def talk_request(request):

    """Takes a user request to find a talk and it returns a json object
    with talk names if the match exists or it returns None as json object"""

    user_input = request.GET.get('talk-name-input')
    if not user_input:
        data = {'matchedTalks': None}
        return JsonResponse(data)
    else:     
        talks = Talk.objects.filter(
                    name__icontains=f'{user_input}').values_list('name', flat=True)
        if talks:        
            data = {'matchedTalks': list(talks)}
            return JsonResponse(data)
        
        else:
            data = {'matchedTalks': 'No results found'}
            return JsonResponse(data)

def get_page(request):
    """This gets the list of objects of the next page. Assists in the pagination on scroll"""

    posts_list = Post.objects.values_list(
                    'talk__name', 'creator__username', 
                    'content', 'date_created')
    paginator = Paginator(posts_list, 4)

    page_num = request.GET.get('page')
    
    try:
        page = paginator.page(page_num)
        context = {'posts':list(page.object_list)}
    except:
        context = {'posts': None}
    return JsonResponse(context)