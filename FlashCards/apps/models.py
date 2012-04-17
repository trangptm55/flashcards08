from django.contrib.auth.models import User
from django.db import models

class InitValue(models.Model):
    name = models.CharField(max_length=255)
    value = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class GradeChoice(models.Model):
    value = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubjectChoice(models.Model):
    f_value = models.PositiveIntegerField(name='First value')
    l_value = models.PositiveIntegerField(name='Last value')
    name = models.CharField(max_length=255)

    def __str__(self):
        if not self.l_value:
            name = self.name
        else:
            name = '%s > %s' % (SubjectChoice.objects.get(f_value=self.f_value, l_value=0).name, self.name)
        return name

    __str__.admin_order_field = ('-f_value', '-l_value')

class Prompt(models.Model):
    prompt = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __unicode__(self):
        return self.prompt

class Flashcard(models.Model):
    flashcard_id = models.CharField(max_length=20, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length = 500 , null = True)
    minGrade = models.CharField(max_length = 255 , null = True)
    maxGrade = models.CharField(max_length = 255 , null = True)
    subject = models.CharField(max_length = 255 , null = True)
    is_public = models.BooleanField()
    prompt = models.ManyToManyField(Prompt, related_name='prompt_set')
    like = models.ManyToManyField(User, related_name='likes')

    def __unicode__(self):
        return self.title

class FlashCard_Set(models.Model):
    user = models.ForeignKey(User)
    Flashcard = models.ForeignKey(Flashcard)
    time = models.DateTimeField()

    #mod = models.ManyToManyField(User)