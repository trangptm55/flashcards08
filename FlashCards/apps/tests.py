# -*- encoding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from apps.models import *
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def testGradeChoice(self):
        n = "Trang"
        v = 3
        choice = GradeChoice(value = v, name = n)

        str = "%s" %choice
        self.assertEqual(choice.value, v)
        self.assertEqual(choice.name, n)
        self.assertEqual(str, n)

    def testSubjectChoice(self):
        n = "Subject"
        v = 3
        subject = SubjectChoice(value = v, name = n)
        str = "%s" %subject

        self.assertEqual(subject.value, v)
        self.assertEqual(subject.name, n)
        self.assertEqual(str, n)

    def testPrompt(self):
        p = "Prompt"
        a = "Answer"

        prompt = Prompt(prompt = p, answer = a)
        self.assertEqual(prompt.prompt, p)
        self.assertEqual(prompt.answer, a)

    def testUnicodePrompt(self):
        t = u'¿Como está usted?'
        a = "Answer"
        newPrompt = Prompt(prompt = t, answer = a)
        self.assertEqual(unicode(newPrompt), u'¿Como está usted?', "Wong Wong Wrong")

class FlashCardTest(TestCase):
    fl_id = "ID"
    title = "Title"
    des = "About a FlashCard"
    min = "Grade1"
    max = "Grade9"
    subject = "Subject"
    is_public = True

    def testUnicode(self):
        t = u'¿Como está usted?'
        flashcard = Flashcard.objects.create(flashcard_id = self.fl_id, title = t, description = self.des, minGrade = self.min, maxGrade = self.max, subject = self.subject, is_public = True)
        self.assertEqual(unicode(flashcard), u'¿Como está usted?')

    def testFlashCard(self):
        flashcard = Flashcard.objects.create(flashcard_id = self.fl_id, title = self.title, description = self.des, minGrade = self.min, maxGrade = self.max, subject = self.subject, is_public = True)
        self.assertEqual(flashcard.flashcard_id, "ID")
        self.assertEqual(flashcard.title, self.title)
        self.assertEqual(flashcard.description, self.des)
        self.assertEqual(flashcard.minGrade, self.min)
        self.assertEqual(flashcard.maxGrade, self.max)
        self.assertEqual(flashcard.subject, "Subject")
