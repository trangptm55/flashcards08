from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from FlashCards.accounts.models import UserProfile
from FlashCards.apps.models import *

def search(request):
    q = request.GET['q']
    # Replace "Multi Space" by single Space
    while '  ' in q:
        q = q.replace("  "," ")

    queries = q.split(' ')
    FCs = FlashCard_Set.objects.all()
    result = []

    # Searching
    for FC in FCs:
        for query in queries:
            if query.lower() in FC.Flashcard.title.lower() and FC not in result:
                result.insert(1, FC)

    # Paginator
    paginator = Paginator(result, InitValue.objects.get(name='per_page').value)
    page = request.GET.get('page') or 1

    try:
        FCs_set = paginator.page(page)
    except PageNotAnInteger:
        FCs_set = paginator.page(1)
    except EmptyPage:
        FCs_set = paginator.page(paginator.num_pages)

    # Username
    if request.user.is_anonymous():
        name = 'Guest'
    else:
        name = request.user.first_name

    # User's avatar
    if not request.user.is_anonymous():
        user_avatar = UserProfile.objects.get(user=request.user).getAvatarUrl()
    else:
        user_avatar = None

    # Side menu
    menu = SubjectChoice.objects.all().order_by('value')

    var = RequestContext(request, {
        'query': q,
        'avatar': user_avatar,
        'FCs': FCs_set,
        'name': name,
        'menu': menu,
    })

    return render_to_response('search.html', var)
