import os
from django.conf.urls.defaults import *
from Allthink.views import *

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

media = os.path.join(
    os.path.dirname(__file__), 'media'
)

urlpatterns = patterns('',

    # Browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    (r'^user/(\w+)/lesson/create/$', create_lesson),
    (r'^user/(\w+)/lesson/(\w+)/view/(\w+)$', view_lesson),
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

    # Session management
    (r'^login/$', login),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': media}),
    (r'^signup/$', register_page),
    (r'^signup/teacher/$', teacher_register_page),
    (r'^files/$', add_doc),
)
