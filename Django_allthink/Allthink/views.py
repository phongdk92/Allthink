# Create your views here.
import os
from ajax_select.fields import AutoCompleteField
import datetime
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import File
from django.core.servers.basehttp import FileWrapper
from django.http import  HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from Allthink.forms import *
from Allthink.models import *
from settings import STATIC_ROOT, MEDIA_ROOT


@login_required
def user_page(request, username):
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'teacher' :
        lessons = user_profile.lesson_set.all()
        variables = RequestContext(request, {
            'username': username,
            'fullname' : user_profile.fullname,
            'lessons': lessons,
            'avatar_dir' : user_profile.avatar.url,
        })
        return  render_to_response('teacher_page.html', variables)
    else :
        all_lessons = Lesson.objects.all()
        lesson_ref = LessonReference.objects.get(user = user_profile)
        lessons = lesson_ref.lessons.all()
        variables = RequestContext(request, {
            'username': username,
            'fullname' : user_profile.fullname,
            'all_lessons': all_lessons,
            'lessons': lessons,
            'avatar_dir' : user_profile.avatar.url,
            })
        return  render_to_response('student_page.html', variables)

def main_page(request):
    return render_to_response(
        'main_page.html', RequestContext(request)
    )

def login(request):
    status='Wellcome !'
    if request.method== "POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            login_username=login_form.cleaned_data['username']
            login_password=login_form.cleaned_data['password']
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None and user.is_active:
                auth.login(request, user)
                check = login_form.cleaned_data['remember_me']
                return HttpResponseRedirect('/user/'+login_username+'/')
            else:
                status="There were some errors with your username and password !"
            variables=RequestContext(request,{
                'form': login_form,
                'status':status,
            })
            return render_to_response('registration/login.html',variables)
    else :
        login_form=LoginForm()
    variables= RequestContext(request,{
        'form':login_form,
        'status':status
    })
    return render_to_response('registration/login.html',variables)

def logout_page(request):
    logout(request)
    return render_to_response('registration/logout.html')

def register_page(request):
    return render_to_response('registration/signup.html', RequestContext(request))

def teacher_register_page(request) :
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            fileinit = open('%s/%s' % (STATIC_ROOT, "images/teacher.jpg"), 'rb')
            filea = File(fileinit)
            filename =filea.name
            name = filename.split('.')
            filea.name = user.username + '_avatar_teacher' + '.'+ name[len(name)-1]
            user_profile = UserProfile.objects.create(
                user = user,
                fullname=form.cleaned_data['fullname'],
                typeUser='teacher',
                avatar = filea,
            )
            filea.close()
            user_profile.save()
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/teacher_signup.html',variables)


def student_register_page(request) :
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            fileinit = open('%s/%s' % (STATIC_ROOT, "images/student.gif"), 'rb')
            filea = File(fileinit)
            filename =filea.name
            name = filename.split('.')
            filea.name = user.username + '_avatar_student' + '.'+ name[len(name)-1]
            user_profile = UserProfile.objects.create(
                user = user,
                fullname=form.cleaned_data['fullname'],
                typeUser='student',
                avatar = filea,
            )
            filea.close()
            user_profile.save()
            LessonReference.objects.create(
                user = user_profile,
            )
            return render_to_response('registration/teacher_signup_success.html', RequestContext(request))
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/student_signup.html',variables)

@login_required
def user_edit_page(request , username) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    status = ''
    if request.method == 'POST':
        post_temp = request.POST.copy()
        post_temp['email'] = user.email
        post_temp['username'] = user.username
        form = EditAccountForm(post_temp)
        if form.is_valid():
            if user.check_password(form.cleaned_data['password0']):
                user.set_password(form.cleaned_data['password1'])
                user.save()
                user_profile.fullname=form.cleaned_data['fullname']
                user_profile.save()
                status = 'noError'
            else :
                status = 'hasError'

        else :
            status = 'inValid'
    form = EditAccountForm(initial={
        'fullname' : user_profile.fullname,
        'email' : user.email,
        'username' : user.username,
    })
    variables = RequestContext(request, {
        'form': form,
        'status' : status,
        'username' : username,
        'fullname' : user_profile.fullname,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('account.html', variables)

@login_required
def user_avatar_page(request , username) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = user_profile.avatar
            file.delete()
            img = request.FILES['uploadFile']
            filename =img.name
            name = filename.split('.')
            img.name = username + '_avatar' + '.'+ name[len(name)-1]
            user_profile.avatar = img
            user_profile.save()

    form = FileUploadForm()
    variables = RequestContext(request, {
        'form': form,
        'username' : username,
        'fullname' : user_profile.fullname,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('avatar.html', variables)

@login_required
def create_lesson(request, username) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    if request.method == 'POST' :
        form = CreateLesson(request.POST)
        if form.is_valid() :
            lesson = Lesson.objects.create(
                user = user_profile,
                lessonTitle = form.cleaned_data['lessonTitle'],
                author = user_profile.fullname,
                gradeLevel = form.cleaned_data['gradeLevel'],
                subject = form.cleaned_data['subject'],
                description = form.cleaned_data['description'],
            )
            variables = RequestContext ( request,{
                'username' : username,
                'fullname' : user_profile.fullname,
                'lesson'   : lesson,
                'avatar_dir' : user_profile.avatar.url,
            })
            return render_to_response('lesson/lesson_edit.html', variables)
    else :
        form = CreateLesson()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
    })
    return render_to_response('lesson/create_lesson.html',variables)

@login_required
def edit_lesson(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    videos = lesson.video_set.all()
    docs = lesson.document_set.all()
    images = lesson.image_set.all()
    steps = lesson.stepbystep_set.all()
    texts = lesson.text_set.all()
    variables = RequestContext ( request,{
        'username' : username,
        'fullname' : user_profile.fullname,
        'avatar_dir' : user_profile.avatar.url,
        'lesson'   : lesson,
        'videos' : videos,
        'docs' : docs,
        'images' : images,
        'steps' : steps,
        'texts' : texts,
    })
    return render_to_response('lesson/lesson_edit.html',variables)

@login_required
def view_lesson(request, username, id, page, stepid) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = id)
    videos = lesson.video_set.all()
    docs = lesson.document_set.all()
    images = lesson.image_set.all()
    old_id = stepid
    if stepid == '0' :
        stepid = '1'
    step = get_object_or_404(StepbyStep, id = stepid)
    eachsteps = step.step_set.all()
    stepbysteps = lesson.stepbystep_set.all()
    steps = ''
    explains = ''
    for eachstep in eachsteps:
        if eachstep.step != '' :
            steps = steps + '##' + eachstep.step
            explains = explains + '##' + eachstep.explain

    texts = lesson.text_set.all()
    variables = RequestContext ( request,{
        'username' : username,
        'typeUser' : user_profile.typeUser,
        'page' : page,
        'fullname' : user_profile.fullname,
        'avatar_dir' : user_profile.avatar.url,
        'lesson'   : lesson,
        'videos' : videos,
        'docs' : docs,
        'images' : images,
        'stepbysteps' : stepbysteps,
        'step': step,
        'steps' : steps,
        'texts' : texts,
        'explains' : explains,
        'stepid' : old_id,
        })
    return render_to_response('lesson/lesson_view.html',variables)

@login_required
@login_required
def delete_lesson(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    videos = lesson.video_set.all()
    for videos in videos :
        videos.delete()

    docs = lesson.document_set.all()
    for doc in docs :
        doc.delete()

    images = lesson.image_set.all()
    for image in images :
        image.delete()

    texts = lesson.text_set.all()
    for text in texts :
        text.delete()

    stepbysteps = lesson.stepbystep_set.all()
    for sbs in stepbysteps :
        sbs.delete()

    lesson.delete()
    return HttpResponseRedirect('/user/' + username)

@login_required
def edit_lesson_info(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = CreateLesson(request.POST)
        if form.is_valid() :
            lesson.lessonTitle = form.cleaned_data['lessonTitle']
            lesson.gradeLevel = form.cleaned_data['gradeLevel']
            lesson.subject = form.cleaned_data['subject']
            lesson.description = form.cleaned_data['description']
            lesson.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit')

    form = CreateLesson(initial={
        'lessonTitle' : lesson.lessonTitle,
        'gradeLevel' : lesson.gradeLevel,
        'subject' : lesson.subject,
        'description' : lesson.description
    })
    variables = RequestContext(request,{
        'form' : form,
        'lesson' : lesson,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/lesson_edit_info.html', variables)

@login_required
def add_video(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddVideoForm(request.POST)
        if form.is_valid() :
            Video.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                url = form.cleaned_data['url'],
                text = form.cleaned_data['text'],
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddVideoForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_video_page.html',variables)

@login_required
def add_doc(request, username, id ) :
    lesson = get_object_or_404(Lesson, id = id)
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    file_docs = user_profile.file_doc_set.all()
    FILES = ((file.id,file.file_name) for file in file_docs)
    if request.method == 'POST' :
        form = AddDocumentForm(request.POST, request.FILES)
        form.fields['selectFile'].choices = FILES
        if form.is_valid() :
            doc = Document.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            f_doc_id = form.cleaned_data['selectFile']
            if f_doc_id :
                f_obj = File_doc.objects.get(id = f_doc_id)
                f_doc_url = f_obj.file.url
                doc.file_doc_id = f_doc_id
                doc.file_doc_url = f_doc_url
                doc.save()
            if request.FILES :
                ufile = request.FILES['uploadFile']
                filename = ufile.name
                name = filename.split('.')
                ufile.name = username + '_' + name[0] + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + '.'+ name[len(name)-1]
                file_doc = File_doc.objects.create(
                    user = user_profile,
                    file = ufile
                )
                doc.file_doc_url = file_doc.file.url
                doc.file_doc_id = file_doc.id
                file_doc.file_name = name[0]+ '.'+ name[len(name)-1]
                file_doc.save()
                doc.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddDocumentForm()
    file_Upload_Form = FileUploadForm()
    form.fields['selectFile'].choices = FILES

    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_ppdoc_page.html',variables)

@login_required
def add_image(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    file_imgs = user_profile.file_img_set.all()
    FILES = ((file.id,file.file_name) for file in file_imgs)
    if request.method == 'POST' :
        form = AddImageForm(request.POST, request.FILES)
        form.fields['selectFile'].choices = FILES
        if form.is_valid() :
            img = Image.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            f_img_id = form.cleaned_data['selectFile']
            if f_img_id :
                f_obj = File_img.objects.get(id = f_img_id)
                f_img_url = f_obj.file.url
                img.file_image_id = f_img_id,
                img.file_image_url = f_img_url,
                img.save()

            if request.FILES :
                ufile = request.FILES['uploadFile']
                filename = ufile.name
                name = filename.split('.')
                ufile.name = username + '_' + name[0] + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + '.'+ name[len(name)-1]
                file_img = File_img.objects.create(
                    user = user_profile,
                    file = ufile
                )
                img.file_image_url = file_img.file.url
                img.file_image_id = file_img.id
                file_img.file_name = name[0]+ '.'+ name[len(name)-1]
                file_img.save()
                img.save()

            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddImageForm()

    file_Upload_Form = FileUploadForm()
    form.fields['selectFile'].choices = FILES

    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_image_page.html',variables)


@login_required
def add_step(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddStepbyStepForm(request.POST)
        if form.is_valid() :

            stepbystep = StepbyStep.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                promt = form.cleaned_data['promt'],
                #step = form.cleaned_data['step'],
                #explain = form.cleaned_data['explain'],
            )
            count = 1
            while count <= 20:
                Step.objects.create(
                    sts = stepbystep,
                    step = form.cleaned_data['step'+str(count)],
                    explain = form.cleaned_data['explain'+str(count)],
                )
                count = count + 1

            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddStepbyStepForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_stepbystep_page.html',variables)

@login_required
def add_text(request, username, id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    lesson = get_object_or_404(Lesson, id = id)
    if request.method == 'POST' :
        form = AddTextForm(request.POST)
        if form.is_valid() :
            Text.objects.create(
                lesson = lesson,
                pageTitle = form.cleaned_data['pageTitle'],
                text = form.cleaned_data['text'],
            )
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id+'/edit/')
    else :
        form = AddTextForm()
    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_text_page.html',variables)

@login_required
def edit_video(request, username, id_lesson, id_video) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    video = get_object_or_404(Video, id = id_video)
    if request.method == 'POST' :
        form = AddVideoForm(request.POST)
        if form.is_valid() :
            video.pageTitle = form.cleaned_data['pageTitle']
            video.url = form.cleaned_data['url']
            video.text = form.cleaned_data['text']
            video.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddVideoForm(initial={
        'pageTitle' : video.pageTitle,
        'url' : video.url,
        'text' : video.text,
    })

    variables = RequestContext(request,{
        'form' : form ,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
    })
    return render_to_response('lesson/add_video_page.html',variables)

@login_required
def edit_doc(request, username, id_lesson , id_doc ) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    doc = get_object_or_404(Document, id = id_doc)
    file_docs = user_profile.file_doc_set.all()
    FILES = ((file.id,file.file_name) for file in file_docs)
    if request.method == 'POST' :
        form = AddDocumentForm(request.POST, request.FILES)
        form.fields['pageTitle'].initial = doc.pageTitle
        form.fields['text'].initial = doc.text
        form.fields['selectFile'].choices = FILES
        form.fields['selectFile'].initial = doc.file_doc_id
        if form.is_valid() :
            f_doc_id = form.cleaned_data['selectFile']
            f_obj = File_doc.objects.get(id = f_doc_id)
            f_doc_url = f_obj.file.url
            doc.pageTitle = form.cleaned_data['pageTitle']
            doc.file_doc_id = f_doc_id
            doc.file_doc_url= f_doc_url
            doc.text = form.cleaned_data['text']

            if  request.FILES :
                ufile = request.FILES['uploadFile']
                filename = ufile.name
                name = filename.split('.')
                ufile.name = username + '_' + name[0] + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + '.'+ name[len(name)-1]
                file_doc = File_doc.objects.create(
                    user = user_profile,
                    file = ufile,
                )
                doc.file_doc_url = file_doc.file.url
                doc.file_doc_id = file_doc.id
                file_doc.file_name = name[0]+ '.'+ name[len(name)-1]
                file_doc.save()
            doc.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddDocumentForm()
    file_Upload_Form = FileUploadForm()
    form.fields['pageTitle'].initial = doc.pageTitle
    form.fields['text'].initial = doc.text
    form.fields['selectFile'].choices = FILES
    form.fields['selectFile'].initial = doc.file_doc_id

    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
    })
    return render_to_response('lesson/add_ppdoc_page.html',variables)

@login_required
def edit_image(request, username, id_lesson, id_image) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    image = get_object_or_404(Image, id = id_image)
    file_imgs = user_profile.file_img_set.all()
    FILES = ((file.id,file.file_name) for file in file_imgs)
    if request.method == 'POST' :
        form = AddImageForm(request.POST, request.FILES)

        form.fields['pageTitle'].initial = image.pageTitle
        form.fields['text'].initial = image.text
        form.fields['selectFile'].choices = FILES
        form.fields['selectFile'].initial = image.file_image_id
        if form.is_valid() :
            f_img_id = form.cleaned_data['selectFile']
            f_obj = File_img.objects.get(id = f_img_id)
            f_img_url = f_obj.file.url
            image.pageTitle = form.cleaned_data['pageTitle']
            image.file_image_id = f_img_id
            image.file_image_url = f_img_url
            image.text = form.cleaned_data['text']

            if  request.FILES :
                ufile = request.FILES['uploadFile']
                filename = ufile.name
                name = filename.split('.')
                ufile.name = username + '_' + name[0] + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + '.'+ name[len(name)-1]
                file_img = File_img.objects.create(
                    user = user_profile,
                    file = ufile
                )
                image.file_image_url = file_img.file.url
                image.file_image_id = file_img.id
                file_img.file_name = name[0] + '.'+ name[len(name)-1]
                file_img.save()
            image.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddImageForm()
    file_Upload_Form = FileUploadForm()
    form.fields['pageTitle'].initial = image.pageTitle
    form.fields['text'].initial = image.text
    form.fields['selectFile'].choices = FILES
    form.fields['selectFile'].initial = image.file_image_id

    variables = RequestContext(request,{
        'form' : form,
        'fileUploadForm' : file_Upload_Form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_image_page.html',variables)

@login_required
def edit_step(request, username, id_lesson, id_step) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    stepbystep = get_object_or_404(StepbyStep, id = id_step)
    steps = stepbystep.step_set.all()
    if request.method == 'POST' :
        form = AddStepbyStepForm(request.POST)
        if form.is_valid() :
            stepbystep.pageTitle = form.cleaned_data['pageTitle']
            stepbystep.promt = form.cleaned_data['promt']
            stepbystep.save()
            count = 0
            while (count<20):
                st = Step.objects.filter(sts__exact = stepbystep)[count]
                st.step = form.cleaned_data['step'+str(count+1)]
                st.explain = form.cleaned_data['explain'+str(count+1)]
                st.save()
                count = count+1
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddStepbyStepForm(initial={
        'pageTitle' : stepbystep.pageTitle,
        'promt' : stepbystep.promt,
        'step1' : steps[0].step,
        'explain1' : steps[0].explain,
        'step2' : steps[1].step,
        'explain2' : steps[1].explain,
        'step3' : steps[2].step,
        'explain3' : steps[2].explain,
        'step4' : steps[3].step,
        'explain4' : steps[3].explain,
        'step5' : steps[4].step,
        'explain5' : steps[4].explain,
        'step6' : steps[5].step,
        'explain6' : steps[5].explain,
        'step7' : steps[6].step,
        'explain7' : steps[6].explain,
        'step8' : steps[7].step,
        'explain8' : steps[7].explain,
        'step9' : steps[8].step,
        'explain9' : steps[8].explain,
        'step10' : steps[9].step,
        'explain10' : steps[9].explain,
        'step11' : steps[10].step,
        'explain11' : steps[10].explain,
        'step12' : steps[11].step,
        'explain12' : steps[11].explain,
        'step13' : steps[12].step,
        'explain13' : steps[12].explain,
        'step14' : steps[13].step,
        'explain14' : steps[13].explain,
        'step15' : steps[14].step,
        'explain15' : steps[14].explain,
        'step16' : steps[15].step,
        'explain16' : steps[15].explain,
        'step17' : steps[16].step,
        'explain17' : steps[16].explain,
        'step18' : steps[17].step,
        'explain18' : steps[17].explain,
        'step19' : steps[18].step,
        'explain19' : steps[18].explain,
        'step20' : steps[19].step,
        'explain20' : steps[19].explain,
        })

    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        #'pageTitle' : stepbystep.pageTitle,
        #'promt' : stepbystep.promt,

    })
    return render_to_response('lesson/add_stepbystep_page.html',variables)

@login_required
def edit_text(request, username, id_lesson, id_text) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    text = get_object_or_404(Text, id = id_text)
    if request.method == 'POST' :
        form = AddTextForm(request.POST)
        if form.is_valid() :
            text.pageTitle = form.cleaned_data['pageTitle']
            text.text = form.cleaned_data['text']
            text.save()
            return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

    form = AddTextForm(initial={
        'pageTitle' : text.pageTitle,
        'text' : text.text,
    })

    variables = RequestContext(request,{
        'form' : form,
        'fullname' : user_profile.fullname,
        'username' : username,
        'avatar_dir' : user_profile.avatar.url,
        })
    return render_to_response('lesson/add_text_page.html',variables)

@login_required
def delete_video(request, username, id_lesson, id_video) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    video = get_object_or_404(Video, id = id_video)
    video.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_doc(request, username, id_lesson, id_doc) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    doc = get_object_or_404(Document, id = id_doc)
#    file = get_object_or_404(File_doc, id = doc.file_doc_url)
#    file.file.delete()
#    file.delete()
    doc.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_image(request, username, id_lesson, id_image) :
    image = get_object_or_404(Image, id = id_image)
#    file = get_object_or_404(File_img, id = image.file_image_url)
#    file.file.delete()
#    file.delete()
    image.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_step(request, username, id_lesson, id_step) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    step = get_object_or_404(StepbyStep, id = id_step)
    step.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def delete_text(request, username, id_lesson, id_text) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    if user_profile.typeUser == 'student' :
        return HttpResponseRedirect('/user/'+username)
    text = get_object_or_404(Text, id = id_text)
    text.delete()
    return HttpResponseRedirect('/user/'+username+'/lesson/'+id_lesson+'/edit/')

@login_required
def student_addref(request, username, lesson_id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = lesson_id)
    lesson_ref = LessonReference.objects.get(user = user_profile)
    lesson_ref.lessons.add(lesson)
    lesson_ref.save()
    return HttpResponseRedirect('/search_form?u='+username)

@login_required
def student_removeref(request, username, lesson_id) :
    user = get_object_or_404(User, username = username)
    user_profile = user.get_profile()
    lesson = get_object_or_404(Lesson, id = lesson_id)
    lesson_ref = LessonReference.objects.get(user = user_profile)
    lesson_ref.lessons.remove(lesson)
    lesson_ref.save()
    return HttpResponseRedirect('/user/'+username)



@login_required
def download_doc_file(request, username, id_doc) :
    doc = get_object_or_404(Document, id = id_doc)
    file = get_object_or_404(File_doc, id = doc.file_doc_id)
    download_name = file.file_name
    download_file = file.file
    response = HttpResponse(FileWrapper(download_file), content_type='application/pdf')
    response['Content-Disposition'] = "attachment;filename=%s"%download_name
    return response


class SearchForm(forms.Form):

    q = AutoCompleteField(
        'lessonLookup',
        #'alookup',
        required=True,
        help_text="",
        label="",
        attrs={'size': 120}
    )

def search_form(request):
    variable = {}
    username = ''
    if 'u' in request.GET:
        username = request.GET.get('u')
    variable['username'] = username
    if 'q' in request.GET:
        key = request.GET.get('q')
        user = get_object_or_404(User, username = username)
        user_profile = user.get_profile()
        lesson_ref = LessonReference.objects.get(user = user_profile)
        variable['entered'] = key
        variable['all_lessons'] = Lesson.objects.filter(lessonTitle__icontains = key).order_by('lessonTitle')
        variable['lessons'] = lesson_ref.lessons.all()
    initial = {'q':""}
    form = SearchForm(initial=initial)
    variable['form'] = form
    return render_to_response('search_form.html',variable,context_instance=RequestContext(request))
