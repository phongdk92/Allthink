import re
from django.contrib.auth.models import  User
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    typeUser = models.CharField(max_length=20)
    fullname = models.CharField(max_length=30)
    avatar = models.FileField(upload_to= 'media/avatar')

class Lesson(models.Model):
    user = models.ForeignKey(UserProfile)
    #
    lessonTitle = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    GRADE_LEVEL = (
        ('all','All grade level') ,
        ('e' , 'Elementary') ,
        ('h' , 'High school') ,
        ('c' , 'College')
    )
    gradeLevel = models.CharField(max_length=30, choices= GRADE_LEVEL)
    SUBJECT = (
        ('math', 'Math'),
        ('science', 'Science'),
        ('physic', 'Physic')
    )
    subject = models.CharField(max_length=30, choices = SUBJECT)
    description = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.lessonTitle

class LessonReference(models.Model):
    user = models.OneToOneField(UserProfile, primary_key=True)
    lessons = models.ManyToManyField(Lesson)


class File_doc(models.Model) :
    user = models.ForeignKey(UserProfile)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to= 'DB/documents')


class File_img(models.Model) :
    user = models.ForeignKey(UserProfile)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to= 'DB/images')

class Video(models.Model):
    lesson = models.ForeignKey(Lesson)
    pageTitle = models.CharField(max_length=100)
    url = models.URLField()
    text = models.TextField(max_length=2000)
    def youtube(self):
        regex = re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})")
        match = regex.match(self.url)
        if not match: return ""
        video_id = match.group('id')
        return video_id

class Document(models.Model):
    lesson = models.ForeignKey(Lesson)
    file_doc = models.CharField(max_length=255)
    pageTitle = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)


class Image(models.Model):
    lesson = models.ForeignKey(Lesson)
    pageTitle = models.CharField(max_length=100)
    file_image = models.CharField(max_length=255)
    text = models.TextField(max_length=2000)


class StepbyStep(models.Model):
    lesson = models.ForeignKey(Lesson)
    pageTitle = models.CharField(max_length=100)
    promt = models.CharField(max_length=300)


class Step(models.Model):
    sts = models.ForeignKey(StepbyStep)
    step = models.CharField(max_length=100)
    explain = models.CharField(max_length=100)


class Text(models.Model):
    lesson = models.ForeignKey(Lesson)
    pageTitle = models.CharField(max_length=100)
    text = models.TextField(max_length=2000)


