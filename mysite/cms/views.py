import datetime

from django.views.decorators.csrf import csrf_exempt
from django import forms



from django.urls import reverse

from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
import datetime
from random import randint
from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book
from mysite.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from cms.models import Teacher, Student, User, Department, Course, Class_of_course, Enrolment, Forum_post
from cms.templates import includes
from cms.forms import Student_profile_form, add_new_student_form, add_new_course_form, add_new_class_of_course_form, \
    student_enrol_in_class_form, add_new_teacher_form, admin_set_dept_head_form, hod_approve_enrolment_form, \
    teacher_post_in_class_forum_form, teacher_set_mark_of_an_enrolment_form, student_see_mark_of_an_enrolment_form








# Create your views here.

@csrf_exempt
def handle_log_in(request, **kwargs):

    print("beginning of handle_log_in")

    current_username = request.session.get( 'username', None )

    print('current_username = ' + str(current_username) )

    if ( current_username is not None ): # user already logged in
        current_user = User.objects.get(username= current_username )
        if ( current_user.user_type == 'ADMIN' ) :
            return render(request, 'admin_homepage.html', { 'username' : current_username } )
        elif ( current_user.user_type == 'TEACHER' ) :
            return render(request, 'teacher_homepage.html', {'username': current_username})
        elif (current_user.user_type == 'STUDENT') :
            return render(request, 'student_homepage.html', {'username': current_username} )

    else: # user not logged in
        if request.method == 'POST' : # one has clicked the login button

            print( 'one has clicked the log in button' )

            username = request.POST.get('username', None)

            print("username = " + username)

            password = request.POST.get('password', None)

            print('password = ' + password)

            try:
                user = User.objects.get( username= username )
            except User.DoesNotExist:
                user = None

            if (user is None or user.password != password): # incorrect username or password
                return render(request, 'login_page.html', {'error': 'Wrong username or password'} )

            else: # correct username and password
                request.session['username'] = username
                request.session['user_type'] = user.user_type

                if ( user.user_type == User.TEACHER ) : # check if the current user is the hod
                    current_teacher = Teacher.objects.get( username= username )
                    if ( current_teacher == current_teacher.dept.head ) :
                        request.session['is_hod'] = True


                return HttpResponseRedirect( reverse('handle_log_in' )  );

        else:  # one has just loaded the page
            return render(request, 'login_page.html', {'error': None} )


def handle_update_profile(request):
    current_username = request.session.get('username', None)
    if (current_username is None): #user not logged in
        return render(request, 'login_page.html', {'error': None})
    else:
        return render(request, 'user_navigation.html', {'error': None})


def handle_change_password(request):
    current_username = request.session.get('username', None)
    if (current_username is None):  # user not logged in
        return render(request, 'login_page.html', {'error': None})
    else:
        return render(request, 'user_navigation.html', {'error': None})


def handle_log_out(request):
    request.session['username'] = None
    request.session['user_type'] = None
    request.session['is_hod'] = False
    return redirect( handle_log_in )
    # return render(request, 'login_page.html', {'error' : False} )


def change_profile_student(request):
    username = request.session.get('username', '')
    student = Student.objects.get(username=username)
    student_profile_form = Student_profile_form(request.POST ,instance=student)
    if student_profile_form.is_valid():
        student_profile_form.save()
    return render(request, 'student_profile_update.html', {'student_profile_form' : student_profile_form})


def handle_add_department(request):
    user_type = request.session.get('user_type', None)
    print('user_type = ' + user_type)
    if user_type == 'ADMIN' : # user is admin

        dept_list = Department.objects.all()

        if request.method == 'POST' : # clicked add button
            department_name = request.POST.get( 'department_name', None )
            same_name_dept_cnt = Department.objects.all().filter( name=department_name ).count()
            if ( same_name_dept_cnt > 0):
                return render(request, 'add_new_department.html', {'error' : 'Dept already exists', 'dept_list' : dept_list} )
            else:
                dept = Department(name=department_name)
                dept.save()
                return render(request, 'add_new_department.html', {'dept_list': dept_list, 'success_message' : 'dept added successfully'} )

        else: # admin just loaded the page
            return render(request, 'add_new_department.html', { 'dept_list' : dept_list } )
    else: # Non admin
        print('user is not admin')
        # return render(request, 'includes/user_navigation.html', {'error': None})
        return render(request, 'permission_denied.html' )


def handle_add_new_student(request):

    user_type = request.session.get('user_type', None)

    print( 'user_type = ' + str(user_type)  )

    if ( user_type != 'ADMIN' ): # Non admin
        print('User is not admin')
        return render(request, 'permission_denied.html')

    else: #user is admin

        if ( request.method == 'POST' ) : #user clicked on the add button

            print('user clicked on the add button')

            form = add_new_student_form(request.POST)



            if ( form.is_valid() ) :

                print( ' form is valid ' )

                username =  form.cleaned_data.get('username', None)

                print( 'username = ' + username )


                password = form.cleaned_data.get('password', None )
                student_id = form.cleaned_data.get( 'studentId', None )
                dept = form.cleaned_data.get('dept', None)
                level = form.cleaned_data.get('level', None)
                term = form.cleaned_data.get( 'term', None )

                user_with_same_username_cnt = User.objects.filter(username= username).count()

                if ( user_with_same_username_cnt > 0 ):
                    return render(request, 'add_new_student.html',
                                  {'add_new_student_form': form, 'error' : 'username already exists'} )

                student_with_same_std_id_cnt = Student.objects.filter( studentId= student_id ).count()

                if ( student_with_same_std_id_cnt > 0 ) :
                    return render(request, 'add_new_student.html',
                                  {'add_new_student_form': form, 'error': 'student id already exists'} )


                student_to_add = form.save(commit=False)
                student_to_add.user_type = 'STUDENT'

                student_to_add.save()

                return render(request, 'add_new_student.html',
                              {'add_new_student_form': form,
                                'message' : 'successfully added student' })


            else: # form is not valid
                return render(request, 'add_new_student.html',
                              {'add_new_student_form': form, 'error': 'form is invalid'})

        else: # user just loaded the page
            form = add_new_student_form()
            return render(request, 'add_new_student.html',
                          { 'add_new_student_form' : form } )



def handle_add_new_course(request):
    user_type = request.session.get('user_type', None)
    if (user_type != 'ADMIN'):  # Non admin
        print('User is not admin')
        return render(request, 'permission_denied.html')

    # user is admin
    print('user is admin')

    # fetch list of all courses
    all_courses_ordered_by_dept = Course.objects.all().order_by( 'dept' )
    print( 'fetched all courses ordered by dept' )


    print( 'request.method = ' + request.method  )

    if (request.method != 'POST')  : # user just loaded the page

        print( 'user just loaded the page' )

        form = add_new_course_form()

        print('created an empty form for adding new course')

        return render(request, 'add_new_course.html', {
            'add_new_course_form' : form,
            'all_courses_ordered_by_dept' : all_courses_ordered_by_dept,

        } )

    print(' user did not load the page just now  ')

    if ( request.method == 'POST' ) : # user clicked on the add_new_course button
        form = add_new_course_form( request.POST )

        if ( not form.is_valid() ) : # invalid form
            return render(request, 'add_new_course.html', {
                'add_new_course_form': form,
                'error' : 'Invalid form',
                'all_courses_ordered_by_dept': all_courses_ordered_by_dept,
            })

        # a valid form submitted

        course = form.save(commit=False)
        course.save()

        new_form = add_new_course_form()
        return render( request, 'add_new_course.html',
                       {
                           'add_new_course_form' : form,
                           'message' : 'Successfully added the course' ,
                            'all_courses_ordered_by_dept': all_courses_ordered_by_dept,
                       })



def handle_add_new_class_of_course(request):
    user_type = request.session.get('user_type', None)
    if (user_type != 'ADMIN'):  # Non admin
        print('User is not admin')
        return render(request, 'permission_denied.html')

    # user is admin
    print( 'user is admin' )

    all_classes = Class_of_course.objects.all().order_by( '-year', '-month' )

    if ( request.method != 'POST' ) : # user didn't click the add button just now
        form = add_new_class_of_course_form()

        return render(request, 'add_new_class_of_course.html', {
            'add_new_class_of_course_form' : form,
            'all_classes' : all_classes,
        } )

    # user clicked the add button
    form = add_new_class_of_course_form( request.POST )

    if (not form.is_valid()):  # invalid form
        return render(request, 'add_new_class_of_course.html', {
            'add_new_class_of_course_form': form,
            'error': 'Invalid form',
            'all_courses_ordered_by_dept': all_classes,
        })

    # a valid form submitted
    class_of_course = form.save()
    # class_of_course.save()

    new_form = add_new_class_of_course_form()
    return render(request, 'add_new_class_of_course.html',
                  {
                      'add_new_class_of_course_form' : form,
                      'message' : 'class successfully added',
                      'all_classes': all_classes,
                  })









def handle_student_enrol_in_class(request):
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'STUDENT'):  # Non student
        print('User is not student')
        return render(request, 'permission_denied.html')

    # user is student
    current_student = Student.objects.get(username= username)

    all_classes = Class_of_course.objects.all()
    classes_student_enrolled_in = current_student.classes_enrolled_in.all()
    classes_available_to_student = all_classes.exclude( pk__in =  classes_student_enrolled_in )

    # print( str(classes_student_enrolled_in) )

    all_enrolments_of_current_student = Enrolment.objects.all( ).filter( student= current_student )

    all_approved_enrolments_of_current_student = all_enrolments_of_current_student.filter( approval_status= Enrolment.APPROVED )
    all_waiting_for_approval_enrolments_of_current_student = all_enrolments_of_current_student.filter(
        approval_status=Enrolment.WAITING_FOR_APPROVAL)
    all_rejected_enrolments_of_current_student = all_enrolments_of_current_student.filter(
        approval_status=Enrolment.REJECTED)





    if ( request.method != 'POST' ) : # user didn't click on the enrol button just now
        student_enrol_in_class_form.base_fields['class_of_course'] = \
            forms.ModelChoiceField(queryset=classes_available_to_student)
        form = student_enrol_in_class_form()
        return render( request, 'student_enrol_in_class.html',
                       {
                          'all_classes' : all_classes,
                           'classes_student_enrolled_in' : classes_student_enrolled_in,
                           'classes_available_to_student' : classes_available_to_student,
                           'all_enrolments_of_current_student' : all_enrolments_of_current_student,
                           'all_approved_enrolments_of_current_student' : all_approved_enrolments_of_current_student,
                           'all_waiting_for_approval_enrolments_of_current_student' : all_waiting_for_approval_enrolments_of_current_student,
                           'all_rejected_enrolments_of_current_student' : all_rejected_enrolments_of_current_student,
                           'student_enrol_in_class_form' : form,
                       }
                        )


    if ( request.method == 'POST' ) : # student clicked on the enrol button just now
        form = student_enrol_in_class_form(request.POST)
        if ( not form.is_valid() ) :
            print( 'Form is not valid' )
            return render(request, 'student_enrol_in_class.html',
                      {
                          'all_classes': all_classes,
                          'classes_student_enrolled_in': classes_student_enrolled_in,
                          'classes_available_to_student': classes_available_to_student,
                          'all_enrolments_of_current_student': all_enrolments_of_current_student,
                          'all_approved_enrolments_of_current_student': all_approved_enrolments_of_current_student,
                          'all_waiting_for_approval_enrolments_of_current_student': all_waiting_for_approval_enrolments_of_current_student,
                          'all_rejected_enrolments_of_current_student': all_rejected_enrolments_of_current_student,
                          'student_enrol_in_class_form': form,
                          'error_message' : 'Can not enrol in this class',
                      }
                      )

        elif ( form.is_valid() ) : # student submitted a valid enrol request
            print('Form is valid')
            new_enrolment = form.save(commit=False)
            new_enrolment.student = current_student
            new_enrolment.save()

            student_enrol_in_class_form.base_fields['class_of_course'] = \
                forms.ModelChoiceField(queryset=classes_available_to_student)
            form = student_enrol_in_class_form()

            return render(request, 'student_enrol_in_class.html',
                          {
                              'all_classes': all_classes,
                              'classes_student_enrolled_in': classes_student_enrolled_in,
                              'classes_available_to_student': classes_available_to_student,
                              'all_enrolments_of_current_student': all_enrolments_of_current_student,
                              'all_approved_enrolments_of_current_student': all_approved_enrolments_of_current_student,
                              'all_waiting_for_approval_enrolments_of_current_student': all_waiting_for_approval_enrolments_of_current_student,
                              'all_rejected_enrolments_of_current_student': all_rejected_enrolments_of_current_student,
                              'student_enrol_in_class_form': form,
                              'success_message': 'Successfully enroled in a class',
                          }
                          )






def teacher_see_list_of_classes_assigned_to(request):
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'TEACHER'):  # Non Teacher
        print('User is not teacher')
        return render(request, 'permission_denied.html')


    # user is a teacher
    current_teacher = Teacher.objects.get( username= username )
    all_classes_current_teacher_assigned_to = current_teacher.class_of_course_set.all()

    context = {'all_classes_current_teacher_assigned_to' : all_classes_current_teacher_assigned_to}
    return render(request, 'teacher_see_list_of_classes_assigned_to.html', context )






def handle_add_new_teacher(request):
    user_type = request.session.get('user_type', None)

    print( 'user_type = ' + str(user_type) )

    if (user_type != 'ADMIN'):  # Non admin
        print('User is not admin')
        return render(request, 'permission_denied.html')

    if ( request.method != 'POST' ) :  # user just loaded the page


        print('user just loaded the page')

        form = add_new_teacher_form()
        return render(request, 'add_new_teacher.html',
                      {'add_new_teacher_form': form})



    if ( request.method == 'POST'):  # user clicked on the add button

        print('user clicked on the add button')

        form = add_new_teacher_form(request.POST)


        if ( not form.is_valid() ) :  # form is not valid

            return render(request, 'add_new_teacher.html',
                      {'add_new_teacher_form': form, 'error': 'form is invalid'})



        # form is valid
        print(' form is valid ')



        username = form.cleaned_data.get('username', None)

        print('username = ' + username)

        password = form.cleaned_data.get('password', None)

        dept = form.cleaned_data.get('dept', None)

        rank = form.cleaned_data.get('rank', None)

        user_with_same_username_cnt = User.objects.filter(username=username).count()

        if (user_with_same_username_cnt > 0):
            return render(request, 'add_new_teacher.html',
                          {'add_new_teacher_form': form, 'error': 'username already exists'})




        teacher_to_add = form.save(commit=False)
        teacher_to_add.user_type = User.TEACHER

        teacher_to_add.save()

        return render(request, 'add_new_teacher.html',
                      {'add_new_teacher_form': form,
                       'message': 'successfully added teacher'})




def admin_set_dept_head(request):
    user_type = request.session.get('user_type', None)

    print('user_type = ' + str(user_type))

    if (user_type != 'ADMIN'):  # Non admin
        print('User is not admin')
        return render(request, 'permission_denied.html')

    form = admin_set_dept_head_form()

    print('request.method = ' + request.method)

    all_dept = Department.objects.all()
    if ( request.method != 'POST' ) : # user just loaded the page

        print('user just loaded the set dept head page')

        return render(request, 'admin_set_department_head.html',
                      {
                          'all_dept' : all_dept,
                          'admin_set_dept_head_form' : form,
                      }
                      )

    if ( request.method == 'POST' ) : #user just clicked on the set button
        dept_pk = request.POST.get('dept', None)
        new_head_pk = request.POST.get('head', None)

        dept = Department.objects.get(pk=dept_pk)
        new_head = Teacher.objects.get(pk=new_head_pk)

        # print('dept = ' + str(dept) )
        # print('new_head = ' + str(new_head) )

        if ( new_head.dept != dept ) : # selected teacher is not in that department
            return render(request, 'admin_set_department_head.html',
                          {
                              'all_dept': all_dept,
                              'admin_set_dept_head_form': form,
                              'error_message' : 'Department head must be from that department'
                          }
                          )



        # everything is alright
        # going to update the database

        dept.head = new_head
        dept.save()

        return render(request, 'admin_set_department_head.html',
                  {
                      'all_dept': all_dept,
                      'admin_set_dept_head_form': form,
                      'success_message' : 'successfully altered the HoD'
                  }
                  )




def hod_approve_new_enrol_request(request):
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    is_hod = request.session.get('is_hod', None)
    if ( (user_type != 'TEACHER') or ( not is_hod ) ):  # Non HoD
        print('User is not HoD')
        return render(request, 'permission_denied.html')

    hod = Teacher.objects.get(username=username)
    dept_of_hod = hod.dept

    all_student_of_this_dept = dept_of_hod.student_set.all()

    all_enrolment_of_this_dept = Enrolment.objects.all().filter(  student__dept=dept_of_hod).order_by( 'student__studentId' )
    all_waiting_for_approval_enrolment_of_this_dept = all_enrolment_of_this_dept.filter( approval_status=Enrolment.WAITING_FOR_APPROVAL )
    all_approved_enrolment_of_this_dept = all_enrolment_of_this_dept.filter( approval_status=Enrolment.APPROVED )
    all_rejected_enrolment_of_this_dept = all_enrolment_of_this_dept.filter(approval_status=Enrolment.REJECTED)




    form = hod_approve_enrolment_form( dept_of_hod )

    print('request.method = ' + request.method)

    if ( request.method != 'POST' ) : # hod just loaded the page
        context =  { 'dept_of_hod' : dept_of_hod,
                     'all_waiting_for_approval_enrolment_of_this_dept' : all_waiting_for_approval_enrolment_of_this_dept,
                     'all_approved_enrolment_of_this_dept' : all_approved_enrolment_of_this_dept,
                     'all_rejected_enrolment_of_this_dept' : all_rejected_enrolment_of_this_dept,
                     'hod_approve_enrolment_form' : form,

                     }
        return render( request, 'hod_approve_enrolment.html', context )



    if ( request.method == 'POST' ) : # hod clicked on the approve or reject button
        covered_enrolments = request.POST.getlist('enrolments_to_deal', None)
        # print( covered_enrolments )
        if 'approve' in request.POST:
            approval_status = Enrolment.APPROVED
        elif 'reject' in request.POST:
            approval_status = Enrolment.REJECTED

        # print( approval_status )
        Enrolment.objects.filter(pk__in=covered_enrolments).update(approval_status=approval_status)



        context = {
            'dept_of_hod': dept_of_hod,
                   'all_waiting_for_approval_enrolment_of_this_dept': all_waiting_for_approval_enrolment_of_this_dept,
                    'all_approved_enrolment_of_this_dept' : all_approved_enrolment_of_this_dept,
                    'all_rejected_enrolment_of_this_dept' : all_rejected_enrolment_of_this_dept,
                   'hod_approve_enrolment_form': form,
                   }
        return render(request, 'hod_approve_enrolment.html', context)




def teacher_post_in_class_forum(request, class_pk) :
    print('start of teacher_post_in_class_forum')
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'TEACHER'):  # Non Teacher
        print('User is not teacher')
        return render(request, 'permission_denied.html')


    current_class_of_course = Class_of_course.objects.get(pk=class_pk)
    print('current_class_of_course = ' + str(current_class_of_course) )
    current_teacher = Teacher.objects.get( username= username )
    print('current_teacher = ' + str(current_teacher)  )


    if ( not current_class_of_course.class_teacher.all().filter( username=username ).exists() ) :
        print('current teacher is not assigned to this course')
        return render(request, 'permission_denied.html')

    # user is a teacher of this class

    form = teacher_post_in_class_forum_form()
    all_forum_post_of_this_class = Forum_post.objects.all().filter(class_of_course=current_class_of_course).order_by(
        '-date_time')
    context = {
        'current_class_of_course': current_class_of_course,
        'all_forum_post_of_this_class': all_forum_post_of_this_class,
        'teacher_post_in_class_forum_form' : form,
    }

    if ( request.method != 'POST' ): # teacher just loaded the page, didn't click on the post button
        return render(request, 'teacher_post_in_class_forum.html', context)


    # user clicked on the post button
    submitted_form = teacher_post_in_class_forum_form(request.POST)

    new_post = submitted_form.save(commit=False)

    new_post.teacher = current_teacher
    new_post.class_of_course = current_class_of_course
    new_post.date_time = datetime.datetime.now()

    new_post.save()


    return render(request, 'teacher_post_in_class_forum.html', context)




def student_see_class_forum(request, class_pk) :
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'STUDENT'):  # Non Teacher
        return render(request, 'permission_denied.html')


    current_class_of_course = Class_of_course.objects.get(pk=class_pk)
    current_student = Student.objects.get( username= username )


    if ( not current_student.classes_enrolled_in.filter(pk=class_pk).exists() ) : # student is not enrolled in the class
        return render(request, 'permission_denied.html')


    # user is a student of this class
    all_forum_post_of_this_class = Forum_post.objects.all().filter(class_of_course=current_class_of_course).order_by(
        '-date_time')
    context = {
        'current_class_of_course': current_class_of_course,
        'all_forum_post_of_this_class': all_forum_post_of_this_class,
    }

    return render(request, 'student_see_class_forum.html', context)


def teacher_see_list_of_students_in_class(request, class_pk) :
    print('start of teacher_post_in_class_forum')
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'TEACHER'):  # Non Teacher
        print('User is not teacher')
        return render(request, 'permission_denied.html')

    current_class_of_course = Class_of_course.objects.get(pk=class_pk)
    print('current_class_of_course = ' + str(current_class_of_course))
    current_teacher = Teacher.objects.get(username=username)
    print('current_teacher = ' + str(current_teacher))

    if (not current_class_of_course.class_teacher.all().filter(username=username).exists()):
        print('current teacher is not assigned to this course')
        return render(request, 'permission_denied.html')


    # user is a teacher of this class
    all_approved_enrolments_of_this_class = Enrolment.objects.all().filter(class_of_course=current_class_of_course,
                                            approval_status=Enrolment.APPROVED).order_by('student__studentId')
    # all_approved_enrolments_of_this_class is sorted by studentId
    context = { 'all_approved_enrolments_of_this_class' : all_approved_enrolments_of_this_class,
                'current_class_of_course' : current_class_of_course,
                }
    return render(request, 'teacher_see_list_of_students_in_class.html', context)


def teacher_set_mark_of_an_enrolment(request, enrolment_pk) :
    print('start of teacher_post_in_class_forum')
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'TEACHER'):  # Non Teacher
        print('User is not teacher')
        return render(request, 'permission_denied.html')

    current_enrolment = Enrolment.objects.get(pk=enrolment_pk)
    current_class_of_course = current_enrolment.class_of_course

    current_teacher = Teacher.objects.get(username=username)
    print('current_teacher = ' + str(current_teacher))

    if (not current_class_of_course.class_teacher.all().filter(username=username).exists()):
        print('current teacher is not assigned to this course')
        return render(request, 'permission_denied.html')


    # user is a teacher of this class
    form = teacher_set_mark_of_an_enrolment_form(instance=current_enrolment)
    context = {'teacher_set_mark_of_a_enrolment_form' : form,
               'current_enrolment' : current_enrolment,
               }
    if ( request.method != 'POST' ): # teacher just loaded the page, didn't click on the update marks
        return render(request, 'teacher_set_mark_of_an_enrolment.html', context)


    # teacher clicked on the update marks button
    submitted_form = teacher_set_mark_of_an_enrolment_form(request.POST or None, instance=current_enrolment)

    if ( submitted_form.is_valid() ) :
        submitted_form.save()
        form = teacher_set_mark_of_an_enrolment_form(instance=current_enrolment)
        context = {'teacher_set_mark_of_a_enrolment_form': form,
                   'current_enrolment': current_enrolment,
                   }
        return render(request, 'teacher_set_mark_of_an_enrolment.html', context)



def student_see_mark_of_an_enrolment(request, enrolment_pk) :
    user_type = request.session.get('user_type', None)
    username = request.session.get('username', None)
    if (user_type != 'STUDENT'):  # Non Student
        return render(request, 'permission_denied.html')

    current_enrolment = Enrolment.objects.get(pk=enrolment_pk)
    current_class_of_course = current_enrolment.class_of_course
    current_student = Student.objects.get(username=username)

    if (not current_enrolment.student==current_student ):  # student is not enrolled in the class
        return render(request, 'permission_denied.html')


    # student is entitled to see mark
    form = student_see_mark_of_an_enrolment_form(instance=current_enrolment)
    context = { 'student_see_mark_of_an_enrolment_form' : form, }
    return render(request, 'student_see_mark_of_an_enrolment.html', context)