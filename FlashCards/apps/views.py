import random
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from FlashCards.apps.forms import *

@login_required
def add_prompt(request):
    if request.method == 'POST':
        title_form = TitleAddForm(request.POST)
        prompt_form = PromptForm(request.POST)
        if title_form.is_valid() & prompt_form.is_valid():
            prompt = None
            flag = True
            while flag:
                value = InitValue.objects.get(name='idrange').value
                try:
                    prompt = Flashcard.objects.create(
                        flashcard_id = random_string(value)
                    )
                    flag = False
                except IntegrityError:
                    InitValue.objects.filter(name='idrange').update(value = value+1)

            prompt.title = request.POST['title']
            prompt.description = request.POST['description']
            prompt.minGrade = prompt.maxGrade = request.POST['grade']
            prompt.subject = request.POST['subject']
            prompt.is_public = True

            for i in xrange(InitValue.objects.get(name='no_prompt').value):
                if request.POST['Prompt_%d' % (i+1)] != '':
                    p = request.POST['Prompt_%d' % (i+1)]
                    a = request.POST['Answer_%d' % (i+1)]

                    prompt.prompt.add(Prompt.objects.create(prompt=p, answer=a))

            prompt.save()

            flash = FlashCard_Set.objects.create(
                user = request.user,
                Flashcard = prompt,
                time = datetime.datetime.now()
            )
            return HttpResponseRedirect('/form')
    else:
        title_form = TitleAddForm()
        prompt_form = PromptForm()
    var = RequestContext(request, {
        'form_title': 'New Flashcards',
        'action':'add',
        'title_form': title_form,
        'prompt_form': prompt_form
    })
    return render_to_response('apps/add_edit_form.html', var)

@login_required
def edit_prompt(request):
    if request.method == 'POST':
        title_form = TitleEditForm(request.POST)
        prompt_form = PromptForm(request.POST)
        if title_form.is_valid() & prompt_form.is_valid():
            prompt = Flashcard.objects.get(flashcard_id = request.POST['flashcard_id_hidden'])

            if not prompt:
                raise Http404('Invalid FlashCard ID')

            for q in prompt.prompt.all():
                q.delete()
            prompt.prompt.clear()

            prompt.title = request.POST['title']
            #prompt.flashcard_id = request.POST['flashcard_id']
            prompt.description = request.POST['description']
            prompt.minGrade = request.POST['minGrade']
            prompt.maxGrade = request.POST['maxGrade']
            prompt.subject = request.POST['subject']
            prompt.is_public = request.POST['is_public']

            for i in xrange(InitValue.objects.get(name='no_prompt').value):
                if request.POST['Prompt_%d' % (i+1)] != '':
                    p = request.POST['Prompt_%d' % (i+1)]
                    a = request.POST['Answer_%d' % (i+1)]

                    prompt.prompt.add(Prompt.objects.create(prompt=p, answer=a))

            prompt.save()

            FlashCard_Set.objects.filter(Flashcard=prompt).update(time=datetime.datetime.now())

            return HttpResponseRedirect('/form')
    else:
        try:
            FC = Flashcard.objects.get(flashcard_id=request.GET.get('id'))
        except ObjectDoesNotExist:
            raise Http404('FlashCard not found')

        if request.user != FlashCard_Set.objects.get(Flashcard=FC).user:
            return HttpResponse('You don\'t have permission to edit this form')

        list = dict([])

        try:
            list['title'] = FC.title
            list['flashcard_id'] = FC.flashcard_id
            list['flashcard_id_hidden'] = FC.flashcard_id
            list['description'] = FC.description
            list['minGrade'] = FC.minGrade
            list['maxGrade'] = FC.maxGrade
            list['subject'] = FC.subject
            list['is_public'] = FC.is_public
            prompts = FC.prompt
            i = 0
            for prompt in prompts.all():
                i += 1
                list['Prompt_%s' % i] = prompt.prompt
                list['Answer_%s' % i] = prompt.answer
        except:
            pass

        title_form = TitleEditForm(list)
        prompt_form = PromptForm(list)

    var = RequestContext(request, {
        'form_title': 'Edit Flashcards',
        'action':'edit',
        'title_form': title_form,
        'prompt_form': prompt_form
    })
    return render_to_response('apps/add_edit_form.html', var)

def delete_prompt(request):
    try:
        FC = Flashcard.objects.get(flashcard_id=request.GET.get('id'))
    except ObjectDoesNotExist:
        raise Http404('FlashCard not found')
    FlashCard_Set.objects.get(Flashcard=FC).delete()
    for q in FC.prompt.all():
        q.delete()
    FC.delete()
    return HttpResponseRedirect('/form')

def show_prompt(request, id):
    FC = get_object_or_404(Flashcard, flashcard_id=id)
    prompts = FC.prompt.order_by('id')
    p = ''
    a = ''
    for prompt in prompts:
        p += prompt.prompt + '***'
        a += prompt.answer + '***'
    p = p[:-3]
    a = a[:-3]
    if request.user in FC.like.filter():
        like = False
    else: like = True
    var = RequestContext(request, {
        'like_no': FC.like.count(),
        'like': like,
        'name': request.user.first_name,
        'FC': FC,
        'prompts': prompts,
        'id' : id,
        'p':p,
        'a':a,
    })
    return render_to_response('apps/show_form.html', var)

def random_string(n):
    """ Create n length random string """
    code = ''.join([random.choice('abcdefghijklmnoprstuvwyxzABCDEFGHIJKLMNOPRSTUVWXYZ0123456789') for i in range(n)])
    return code

def test(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/')
    u = User.objects.get(username__exact=request.user.username)
    u.set_password('0918273645')
    u.save()
    name = request.user.first_name
    return render_to_response('base_home.html', RequestContext(request, {
        'show_topnav':True,
        'name': name
    }))
