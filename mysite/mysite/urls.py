"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import hello, my_homepage_view, default_view, current_datetime, hours_ahead, ua_display_good2, \
    display_meta, contact

# from books import views
from cms.views import handle_log_in, handle_log_out, handle_update_profile, handle_change_password, handle_add_department, \
    handle_add_new_student, handle_add_new_course, handle_add_new_class_of_course, handle_student_enrol_in_class, \
    handle_add_new_teacher, admin_set_dept_head, teacher_see_list_of_classes_assigned_to, hod_approve_new_enrol_request, \
    teacher_post_in_class_forum, student_see_class_forum, teacher_see_list_of_students_in_class, teacher_set_mark_of_an_enrolment, \
    student_see_mark_of_an_enrolment, serve_file_of_forum_post, teacher_add_submission_window, \
    student_see_submissions_of_an_enrolment, serve_file_of_submission, student_edit_submission, \
    teacher_see_submissions_of_a_window

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^hello/$', hello, name='hello'),
    url(r'^$', my_homepage_view, name='my_homepage_view'),
    url(r'^time/$', current_datetime, name='current_datetime'),
    url(r'^time/plus/(\d{1,2})/(\d{1,2})/$', hours_ahead, name='hours_ahead'),
    url(r'^ua_display/$', ua_display_good2, name='ua_display_good2'),
    url(r'^display_meta/$', display_meta, name='display_meta'),
    # url(r'^search-form/$', views.search_form, name='views.search_form'),
    # url(r'^search/$', views.search, name='views.search'),
    #url(r'.', default_view, name='default_view'),
    url(r'^contact/$', contact, name='contact'),



    ########### From here starts our cms app's url
    url(r'^login/$', handle_log_in, name='handle_log_in'),
    url(r'^logout/$', handle_log_out, name='handle_log_out'),
    url(r'^change-password', handle_change_password, name='handle_change_password'),
    url(r'^update-profile', handle_update_profile, name='handle_update_profile'),

    ###### download part
    url(r'^media/forum_post/(?P<forum_post_pk>[0-9]+)/$', serve_file_of_forum_post, name='serve_file_of_forum_post'),
url(r'^media/submission/(?P<submission_pk>[0-9]+)/$', serve_file_of_submission, name='serve_file_of_submission'),


    # admin part
    url(r'^add-new-department', handle_add_department,name='handle_add_department'),
    url(r'^add-new-student', handle_add_new_student, name='handle_add_new_student'),
    url(r'^add-new-teacher', handle_add_new_teacher, name='handle_add_new_teacher'),
    url(r'^add-new-course', handle_add_new_course, name='handle_add_new_course'),
    url(r'^add-new-class-of-course', handle_add_new_class_of_course, name='handle_add_new_class_of_course'),
    url(r'^admin-set-department-head', admin_set_dept_head, name='admin_set_dept_head'),


    # student part
    url( r'^student-enrol-in-class', handle_student_enrol_in_class, name='handle_student_enrol_in_class' ),
    url(r'^student-see-class-forum/(?P<class_pk>[0-9]+)/$', student_see_class_forum, name='student_see_class_forum'),
    url(r'^student-see-mark-of-an-enrolment/(?P<enrolment_pk>[0-9]+)/$', student_see_mark_of_an_enrolment,
        name='student_see_mark_of_an_enrolment'),
    url(r'^student-see-submissions-of-an-enrolment/(?P<enrolment_pk>[0-9]+)/$', student_see_submissions_of_an_enrolment,
        name='student_see_submissions_of_an_enrolment'),
    url(r'^student-edit-submission/(?P<submission_pk>[0-9]+)/$', student_edit_submission, name='student_edit_submission'),





    # teacher part
    url(r'teacher-see-list-of-classes-assigned-to', teacher_see_list_of_classes_assigned_to,
        name='teacher_see_list_of_classes_assigned_to'),
    url(r'teacher-post-in-class-forum/(?P<class_pk>[0-9]+)/$', teacher_post_in_class_forum, name='teacher_post_in_class_forum'),
    url(r'teacher-see-list-of-students-in-class/(?P<class_pk>[0-9]+)/$', teacher_see_list_of_students_in_class,
        name='teacher_see_list_of_students_in_class'),
    url(r'teacher-set-mark-of-an-enrolment/(?P<enrolment_pk>[0-9]+)/$', teacher_set_mark_of_an_enrolment,
        name='teacher_set_mark_of_an_enrolment'),
    url(r'teacher-add-submission-window/(?P<class_pk>[0-9]+)/$', teacher_add_submission_window, name='teacher_add_submission_window'),
    url(r'teacher-see-submissions-of-a-window/(?P<submission_window_pk>[0-9]+)/$', teacher_see_submissions_of_a_window,
        name='teacher_see_submissions_of_a_window'),





        # hod part
        url(r'hod-approve-enrolment', hod_approve_new_enrol_request, name='hod_approve_new_enrol_request'),





    # url(r'^student_profile_update/$', change_profile_student, name='change_profile_student'),
    



]
