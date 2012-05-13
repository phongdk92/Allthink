import os
from django.conf.urls.defaults import *
from Allthink.views import *
from django.contrib import admin
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

media = os.path.join(
    os.path.dirname(__file__), 'media'
)

db_media = os.path.join(
    os.path.dirname(__file__), 'DB/images'
)

urlpatterns = patterns('',

    # Browsing for Teacher
    (r'^$', main_page),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^user/(\w+)/$', user_page),
    (r'^user/(\w+)/lesson/create/$', create_lesson),
    (r'^user/(\w+)/lesson/(\w+)/view/(\w+)/(\w+)/$', view_lesson),
    (r'^user/(\w+)/lesson/(\w+)/edit/$', edit_lesson),
    (r'^user/(\w+)/lesson/(\w+)/delete/$', delete_lesson),
    (r'^user/(\w+)/lesson/(\w+)/edit-info/$', edit_lesson_info),

    (r'^user/(\w+)/lesson/(\w+)/add-video/$', add_video),
    (r'^user/(\w+)/lesson/(\w+)/add-doc/$', add_doc),
    (r'^user/(\w+)/lesson/(\w+)/add-image/$', add_image),
    (r'^user/(\w+)/lesson/(\w+)/add-step/$', add_step),
    (r'^user/(\w+)/lesson/(\w+)/add-text/$', add_text),

    (r'^user/(\w+)/lesson/(\w+)/video/(\w+)/edit/$', edit_video),
    (r'^user/(\w+)/lesson/(\w+)/doc/(\w+)/edit/$', edit_doc),
    (r'^user/(\w+)/lesson/(\w+)/image/(\w+)/edit/$', edit_image),
    (r'^user/(\w+)/lesson/(\w+)/step/(\w+)/edit/$', edit_step),
    (r'^user/(\w+)/lesson/(\w+)/text/(\w+)/edit/$', edit_text),

    (r'^user/(\w+)/lesson/(\w+)/video/(\w+)/delete/$', delete_video),
    (r'^user/(\w+)/lesson/(\w+)/doc/(\w+)/delete/$', delete_doc),
    (r'^user/(\w+)/lesson/(\w+)/image/(\w+)/delete/$', delete_image),
    (r'^user/(\w+)/lesson/(\w+)/step/(\w+)/delete/$', delete_step),
    (r'^user/(\w+)/lesson/(\w+)/text/(\w+)/delete/$', delete_text),

    # Download file
    (r'^user/(\w+)/download/(\w+)/$', download_doc_file),

    # Browsing for student
    (r'^user/(\w+)/lesson/(\w+)/addref/$', student_addref),
    (r'^user/(\w+)/lesson/(\w+)/removeref/$', student_removeref),
    # Session management
    (r'^login/$', login),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': media}),
    (r'^DB/images/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': db_media}),
    (r'^signup/$', register_page),
    (r'^signup/teacher/$', teacher_register_page),
    (r'^signup/student/$', student_register_page),
    url(r'^search_form',  view='Allthink.views.search_form',name='search_form'),
    (r'^admin/lookups/', include(ajax_select_urls)),
    (r'^user/(\w+)/account/$', user_edit_page),
    (r'^user/(\w+)/pic/$', user_avatar_page),
    (r'^files/$', add_doc),
)
