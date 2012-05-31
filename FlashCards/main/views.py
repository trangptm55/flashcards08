# coding=utf-8
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from FlashCards import settings
from FlashCards.accounts.forms import LoginForm
from FlashCards.accounts.models import UserProfile
from FlashCards.apps.views import *
from FlashCards.search.views import search

def main_page(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/app/')
    return render_to_response('main_page.html', RequestContext(request, {
        'show_topnav': True,
        'head_title': 'Group8 - K55CA - SE'
    }))

@login_required
def user_page(request):
    if request.GET.has_key('u'):
        f_user = User.objects.get(username=request.GET['u'])
    else: f_user=request.user

    if request.user.is_anonymous():
        name = 'Guest'
    else:
        name = request.user.first_name
    avatar = UserProfile.objects.get(user=request.user).getAvatarUrl()
    f_avatar = UserProfile.objects.get(user=f_user).getAvatarUrl()
    return render_to_response('main/user_page.html', RequestContext(request, {
        'head_title': 'Flashcards',
        'avatar': avatar,
        'f_avatar': f_avatar,
        'username': request.user.username,
        'name': name,
        'f_user': f_user,
        'path': request.META['QUERY_STRING']
    }))

@login_required
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
        flashcards = FlashCard_Set.objects.filter(owner=user).order_by('-time')
        var = RequestContext(request, {
            'u': user,
            'flashcards': flashcards,
            })
        return render_to_response('main/iframe_list.html', var)

@login_required
def like(request, id):
    try:
        FC = Flashcard.objects.get(flashcard_id=id)
    except ObjectDoesNotExist:
        return Http404('Invalid Flashcard ID')
    FC.like.add(request.user)
    FC.save()
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')


def dir_subj(request, subj_id):
    if subj_id != 'all':
        FCs = Flashcard.objects.filter(subject=subj_id, is_public=True)
    else: FCs = Flashcard.objects.filter(is_public=True)
    FCs_set_list = []
    for FC in FCs:
        FCs_set_list.append(FlashCard_Set.objects.get(Flashcard=FC))

    # Paginator
    FCs_set_list.sort(key=lambda FC: FC.Flashcard.like.count(), reverse=True)
    paginator = Paginator(FCs_set_list, InitValue.objects.get(name='per_page').value)
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

    if subj_id != 'all':
        current = SubjectChoice.objects.get(value=subj_id)
        head_title = current.name
    else:
        current = {'name': 'All Subjects', 'value': '0'}
        head_title = 'All Subjects'


    var = RequestContext(request, {
        'head_title': head_title,
        'avatar': user_avatar,
        'FCs': FCs_set,
        'name': name,
        'menu': menu,
        'subj': current
    })
    return render_to_response('main/dir_subj.html', var)


def dir_page(request):
    if request.GET.has_key('q'):
        return search(request)
    subjects = SubjectChoice.objects.all()

    FC_set = []
    for subject in subjects:
        FCs = Flashcard.objects.filter(subject=subject.value, is_public=True)
        FCs = sorted(FCs, key=lambda FC: FC.like.count(), reverse=True)[:5]
        FC_set.append({'subject': subject, 'flashcard': FCs})

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

    menu = SubjectChoice.objects.all().order_by('value')
    return render_to_response('main/dir_page.html', RequestContext(request, {
        'head_title': 'All Flashcards',
        'avatar': user_avatar,
        'name': name,
        'menu': menu,
        'FC_set': FC_set,
        }))

def random_number_challenge():
    chars, ret = u'0123456789', u''
    for i in range(settings.CAPTCHA_LENGTH):
        ret += random.choice(chars)
    return ret.upper(), ret


def init(request):
    user = User.objects.get(is_superuser=True)
    if user.first_name == '' or not user.first_name:
        user.first_name = 'admin'
        user.save()
    try:
        UserProfile.objects.get_or_create(user=user)
    except :
        pass
    if not InitValue.objects.filter(name='idrange').count():
        InitValue.objects.create(name='idrange', value=5)
    if not InitValue.objects.filter(name='no_prompt').count():
        InitValue.objects.create(name='no_prompt', value=5)
    if not InitValue.objects.filter(name='per_page'):
        InitValue.objects.create(name='per_page', value=10)
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
        SubjectChoice.objects.create(value=26, name='Art')
        SubjectChoice.objects.create(value=19, name='Business & Economics')
        SubjectChoice.objects.create(value=39, name='Computer Science')
        SubjectChoice.objects.create(value=40, name='Geography')
        SubjectChoice.objects.create(value=36, name='Government & Politics')
        SubjectChoice.objects.create(value=44, name='History')
        SubjectChoice.objects.create(value=12, name='Math')
        SubjectChoice.objects.create(value=25, name='Music')
        SubjectChoice.objects.create(value=42, name='Foreign Language')
        SubjectChoice.objects.create(value=1, name='English/Language Arts')
        SubjectChoice.objects.create(value=5, name='Science')
        SubjectChoice.objects.create(value=41, name='PE & Health')
        SubjectChoice.objects.create(value=18, name='Religion')
        SubjectChoice.objects.create(value=99, name='Other')

    return HttpResponseRedirect('/')


def test(request):
    pass