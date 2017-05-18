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
    handle_add_new_teacher, admin_set_dept_head

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



    # admin part
    url(r'^add-new-department', handle_add_department,name='handle_add_department'),
    url(r'^add-new-student', handle_add_new_student, name='handle_add_new_student'),
    url(r'^add-new-teacher', handle_add_new_teacher, name='handle_add_new_teacher'),
    url(r'^add-new-course', handle_add_new_course, name='handle_add_new_course'),
    url(r'^add-new-class-of-course', handle_add_new_class_of_course, name='handle_add_new_class_of_course'),
    url(r'^admin-set-department-head', admin_set_dept_head, name='admin_set_dept_head'),


    # student part
    url( r'^student-enrol-in-class', handle_student_enrol_in_class, name='handle_student_enrol_in_class' )





    # teacher part




    # url(r'^student_profile_update/$', change_profile_student, name='change_profile_student'),
]
