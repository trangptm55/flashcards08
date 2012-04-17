# coding=utf-8
from django import forms
from FlashCards.apps.models import *

GRADE_CHOICES = [
    ('', 'Select...'),
]
for grade in GradeChoice.objects.filter().order_by('-value'):
    GRADE_CHOICES.insert(1, (grade.value, grade.name))

SUBJECT_CHOICES = [
    ('', 'Select...'),
]

for s in SubjectChoice.objects.filter().order_by('-f_value', '-l_value'):
    if not s.l_value:
        name = s.name
    else:
        name = SubjectChoice.objects.get(f_value=s.f_value, l_value=0).name + u' › ' + s.name
    SUBJECT_CHOICES.insert(1, (u'%s-%s' % (s.f_value, s.l_value), name) )

class TitleAddForm(forms.Form):
    title = forms.CharField(
        label='Flashcard Title',
        max_length=200,
        widget=forms.TextInput(attrs={'size':28})
    )
    flashcard_id = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        label=''
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs = {'cols': 65, 'rows': 2}),
        required = False
    )
    grade = forms.ChoiceField(
        label='Grade Level',
        choices = GRADE_CHOICES,
    )
    subject = forms.ChoiceField(
        choices = SUBJECT_CHOICES,
    )

class TitleEditForm(forms.Form):
    title = forms.CharField(
        label='Flashcard Title',
        max_length=200,
        widget=forms.TextInput(attrs={'size':28})
    )
    flashcard_id_hidden = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
        label=''
    )
    flashcard_id = forms.CharField(
        required=False,
        label='Flashcard ID'
    )
    minGrade = forms.ChoiceField(
        label='Min. Grade Level',
        choices = GRADE_CHOICES,
    )
    maxGrade = forms.ChoiceField(
        label='Max. Grade Level',
        choices = GRADE_CHOICES,
    )
    subject = forms.ChoiceField(
        choices = SUBJECT_CHOICES,
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs = {'cols': 65, 'rows': 2}),
        required = False
    )
    is_public = forms.BooleanField(
        label='List in public directory'
    )

class PromptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PromptForm, self).__init__(*args, **kwargs)
        for i in xrange(InitValue.objects.get(name='no_prompt').value):
            if i < 9:
                self.fields['Prompt_%d' % (i+1)] = forms.CharField(label='Prompt 0%d' % (i+1), required=False)
                self.fields['Prompt_%d' % (i+1)].widget.attrs = {'name': 'q%s' % i, 'size':40}
                self.fields['Answer_%d' % (i+1)] = forms.CharField(label='Answer 0%d' % (i+1), required=False)
                self.fields['Answer_%d' % (i+1)].widget.attrs = {'name': 'a%s' % i, 'size':20}
            else:
                self.fields['Prompt_%d' % (i+1)] = forms.CharField(required=False)
                self.fields['Prompt_%d' % (i+1)].widget.attrs = {'name': 'q%s' % i, 'size':40}
                self.fields['Answer_%d' % (i+1)] = forms.CharField(required=False)
                self.fields['Answer_%d' % (i+1)].widget.attrs = {'name': 'a%s' % i, 'size':20}
