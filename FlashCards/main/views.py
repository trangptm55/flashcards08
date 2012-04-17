# coding=utf-8
from FlashCards.apps.views import *

def main_page(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/user/')
    return render_to_response('main_page.html', RequestContext(request, {
        'show_topnav':True,
        'head_title': 'Group8 - K55CA - SE'
    }))

def user_page(request):
    try:
        para = '?' + request.get_full_path().split('?')[1]
    except:
        para = ''
    if request.user.is_anonymous():
        name = 'Anonymous'
    else:
        name = request.user.first_name
    return render_to_response('main/user_page.html', RequestContext(request, {
        'username': request.user.username,
        'name': name,
        'para': para
    }))

def flashcard_page(request):
    action = None
    if request.GET.has_key('u'):
        user = User.objects.get(username=request.GET['u'])
    else:
        user = request.user

    if request.GET.has_key('action'):
        action = request.GET['action']

    if action == 'add':
        return add_prompt(request)
    elif action == 'edit':
        return edit_prompt(request)
    elif action == 'delete':
        return delete_prompt(request)
    else:
        flashcards = FlashCard_Set.objects.filter(user=user).order_by('-time')
        var = RequestContext(request, {
            'flashcards': flashcards,
            })
        return render_to_response('main/iframe_list.html', var)

def like(request, id):
    try:
        FC = Flashcard.objects.get(flashcard_id = id)
    except ObjectDoesNotExist:
        return Http404('Invalid Flashcard ID')
    FC.like.add(request.user)
    FC.save()
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')

def dir_subj(request, subj):
    pass

def dir_page(request):
    pass

def init(request):
    if not InitValue.objects.filter(name='idrange').count():
        InitValue.objects.create(name='idrange', value=5)
    if not InitValue.objects.filter(name='no_prompt').count():
        InitValue.objects.create(name='no_prompt', value=5)
    if not GradeChoice.objects.count():
        GradeChoice.objects.create(value='0', name='Kindergarten/Pre-K')
        GradeChoice.objects.create(value='1', name='1st Grade')
        GradeChoice.objects.create(value='2', name='2nd Grade')
        GradeChoice.objects.create(value='3', name='3rd Grade')
        GradeChoice.objects.create(value='4', name='4th Grade')
        GradeChoice.objects.create(value='5', name='5th Grade')
        GradeChoice.objects.create(value='6', name='6th Grade')
        GradeChoice.objects.create(value='7', name='7th Grade')
        GradeChoice.objects.create(value='8', name='8th Grade')
        GradeChoice.objects.create(value='9', name='9th Grade')
        GradeChoice.objects.create(value='10', name='10th Grade')
        GradeChoice.objects.create(value='11', name='11th Grade')
        GradeChoice.objects.create(value='12', name='12th Grade')
        GradeChoice.objects.create(value='13', name='College')
        GradeChoice.objects.create(value='14', name='Occupational')
        GradeChoice.objects.create(value='99', name='Other')
    if not SubjectChoice.objects.count():
        SubjectChoice.objects.create(f_value=26, l_value=0, name='Art')
        SubjectChoice.objects.create(f_value=19, l_value=0, name='Business & Economics')
        SubjectChoice.objects.create(f_value=39, l_value=0, name='Computer Science')
        SubjectChoice.objects.create(f_value=40, l_value=0, name='Geography')
        SubjectChoice.objects.create(f_value=36, l_value=0, name='Government & Politics')
        SubjectChoice.objects.create(f_value=44, l_value=0, name='History')
        SubjectChoice.objects.create(f_value=44, l_value=17, name='American')
        SubjectChoice.objects.create(f_value=44, l_value=21, name='Europe')
        SubjectChoice.objects.create(f_value=44, l_value=24, name='World')
        SubjectChoice.objects.create(f_value=12, l_value=0, name='Math')
        SubjectChoice.objects.create(f_value=12, l_value=13, name='Algebra')
        SubjectChoice.objects.create(f_value=12, l_value=45, name='Arithmetic')
        SubjectChoice.objects.create(f_value=12, l_value=14, name='Calculus')
        SubjectChoice.objects.create(f_value=12, l_value=16, name='Statistics')
        SubjectChoice.objects.create(f_value=25, l_value=0, name='Music')
        SubjectChoice.objects.create(f_value=42, l_value=0, name='Foreign Language')
        SubjectChoice.objects.create(f_value=42, l_value=28, name='English (ESL)')
        SubjectChoice.objects.create(f_value=42, l_value=30, name='French')
        SubjectChoice.objects.create(f_value=42, l_value=35, name='Spanish')
        SubjectChoice.objects.create(f_value=1, l_value=0, name='English/Language Arts')
        SubjectChoice.objects.create(f_value=5, l_value=0, name='Science')
        SubjectChoice.objects.create(f_value=5, l_value=6, name='Biology')
        SubjectChoice.objects.create(f_value=5, l_value=7, name='Chemistry')
        SubjectChoice.objects.create(f_value=5, l_value=8, name='Earth Science')
        SubjectChoice.objects.create(f_value=5, l_value=10, name='Physics')
        SubjectChoice.objects.create(f_value=5, l_value=11, name='Psychology')
        SubjectChoice.objects.create(f_value=5, l_value=20, name='Medicine')
        SubjectChoice.objects.create(f_value=41, l_value=0, name='PE & Health')
        SubjectChoice.objects.create(f_value=18, l_value=0, name='Religion')
        SubjectChoice.objects.create(f_value=99, l_value=0, name='Other')

    return HttpResponseRedirect('/')