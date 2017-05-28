from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    address = models.CharField(max_length=200, default="", blank=True)
    phone_num = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(null=True, blank=True)


    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'
    ADMIN = 'ADMIN'

    USER_TYPE = (
        ( 'TEACHER', 'Teacher' ),
        ( 'STUDENT', 'Student' ),
        ( 'ADMIN', 'Admin' )
    )
    user_type = models.CharField(max_length=200, choices=USER_TYPE)

    def __str__(self):
        return "user : " + self.username + ", user type : " + self.user_type


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + ' ( head = ' + str(self.head) + ' )'

    def clean(self):
        if ( self.head is not models.null ) :
            dept_of_head = self.head.dept
            if ( dept_of_head != self ) :
                raise ValidationError('Department head must be teacher of same department')






class Teacher(User):
    PROFESSOR = 'PROFESSOR'
    ASSOCIATE_PROF = 'ASSOCIATE_PROF'
    ASSISTANT_PROF = 'ASSISTANT_PROF'
    LECTURER = 'LECTURER'

    RANKS = (
        (PROFESSOR, 'Professor'),
        (ASSOCIATE_PROF, 'Associate Professor'),
        (ASSISTANT_PROF, 'Assistant Professor'),
        (LECTURER, 'Lecturer')
    )
    joinDate = models.DateField(null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    rank = models.CharField(max_length=200, blank=True, choices=RANKS)

    def __str__(self):
        return 'username = ' + self.username + ', name = ' + self.first_name + " " + self.last_name + ', dept = ' + self.dept.name



class Student(User):
    BARISHAL = 'BARISHAL'
    CHITTAGONG = 'CHITTAGONG'
    DHAKA = 'DHAKA'
    MYMENSINGH = 'MYMENSINGH'
    KHULNA = 'KHULNA'
    RAJSHAHI = 'RAJSHAHI'
    RANGPUR = 'RANGPUR'
    SYLHET = 'SYLHET'
    DIVISION = (
        (BARISHAL, 'Barishal'),
        (CHITTAGONG, 'Chittagong'),
        (DHAKA, 'Dhaka'),
        (MYMENSINGH, 'Mymensingh'),
        (KHULNA, 'Khulna'),
        (RAJSHAHI, 'Rajshahi'),
        (RANGPUR, 'Rangpur'),
        (SYLHET, 'Sylhet')
    )
    studentId = models.CharField(max_length=200, unique=True)
    division = models.CharField(max_length=200, null=True, choices=DIVISION, blank=True )
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(null=True, validators=[MinValueValidator(1),
                                           MaxValueValidator(5)])
    term = models.IntegerField(null=True, validators=[MinValueValidator(1),
                                          MaxValueValidator(2)])
    classes_enrolled_in = models.ManyToManyField( 'Class_of_course', through='Enrolment' )
    dues = models.IntegerField( default=0 )


    def __str__(self):
        user_string = super(Student, self).__str__()
        ret = user_string + ' std_id = ' + self.studentId + '; '
        return ret




class Course(models.Model):
    course_num = models.CharField(max_length=200, null=True, unique=True)
    course_name = models.CharField(max_length=200, null=True)
    credit_hour = models.IntegerField(null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.course_num + ' - ' + self.course_name + ', \n' + 'credit hr = ' + str(self.credit_hour) + ', \n'  \
                + ' dept = ' + self.dept.name





class Class_of_course(models.Model):
    JANUARY = 'January'
    JULY = 'July'
    SESSION_MONTH = (
        (JANUARY, 'January'),
        (JULY, 'July')
    )
    month = models.CharField(max_length=200, choices=SESSION_MONTH, null=True)
    year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2020)])
    course_of_class = models.ForeignKey( Course )
    class_teacher = models.ManyToManyField( Teacher )

    class Meta:
        unique_together = ( 'month', 'year', 'course_of_class' )

    def __str__(self):
        class_teacher_list = self.class_teacher.all()
        ret =  self.month + ' - ' + str(self.year) + ', ' + self.course_of_class.course_num + ' - ' + \
                self.course_of_class.course_name + ' ( '
        for teacher in class_teacher_list :
            ret += ( teacher.__str__() + '; ' )
        ret += ')'

        return ret



class Forum_post(models.Model):
    teacher = models.ForeignKey(Teacher)
    class_of_course = models.ForeignKey(Class_of_course)
    headline = models.CharField( max_length=999, validators=[MinLengthValidator(1)] )
    text = models.TextField( max_length=9999, validators=[MinLengthValidator(1)] )
    date_time = models.DateTimeField(null=True)
    document = models.FileField(upload_to='forum_post/', null=True)





########  I am skipping Department head log table. I think it is unnecessary.


#### Django doesn't need any relation table unless there are some attributes of relation...  I am skipping following tables
# Class_teacher
#
class Enrolment(models.Model):
    student = models.ForeignKey(Student)
    class_of_course = models.ForeignKey(Class_of_course)


    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    WAITING_FOR_APPROVAL = 'WAITING_FOR_APPROVAL'

    APPROVAL_STATUS = (
        ( APPROVED, 'Approved' ),
        ( REJECTED, 'Rejected' ),
        ( WAITING_FOR_APPROVAL, 'Waiting for approval' )
    )
    approval_status = models.CharField(max_length=200, choices=APPROVAL_STATUS, default=WAITING_FOR_APPROVAL)

    ct1_marks = models.IntegerField(default=0)
    ct2_marks = models.IntegerField(default=0)
    ct3_marks = models.IntegerField(default=0)
    ct4_marks = models.IntegerField(default=0)
    ct5_marks = models.IntegerField(default=0)
    ct6_marks = models.IntegerField(default=0)
    assignment1_marks = models.IntegerField(default=0)
    assignment2_marks = models.IntegerField(default=0)
    assignment3_marks = models.IntegerField(default=0)
    attendance_marks = models.IntegerField(default=0)
    term_final_marks = models.IntegerField(default=0)
    viva1_marks = models.IntegerField(default=0)
    viva2_marks = models.IntegerField(default=0)
    experiment_marks = models.IntegerField(default=0)

    other = models.IntegerField(default=0)

    final_out_of_hundred = models.IntegerField(default=0)

    class Meta:
        unique_together = ( 'student', 'class_of_course' )


    def __str__(self):
        return 'student = ' + str(self.student) + '; class_of_course = ' + str(self.class_of_course) + '; '



######  following tables are for vote
class Question_of_vote(models.Model):
    question = models.CharField(max_length=500)
    respodent_type = models.CharField(max_length=400,  null=True)


class Option_of_vote(models.Model):
    question = models.ForeignKey( Question_of_vote )
    option = models.CharField(max_length=500, null=True)


class Response_of_vote(models.Model):
    question = models.ForeignKey( Question_of_vote )
    option = models.ForeignKey( Option_of_vote )
    teacher = models.ForeignKey( Teacher, null=True )
    student = models.ForeignKey( Student, null=True )


    class Meta:
        unique_together = ( ('question', 'teacher', 'student'), )




class Submission_window(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_of_course = models.ForeignKey(Class_of_course, on_delete=models.CASCADE)
    headline = models.CharField(max_length=999, validators=[MinLengthValidator(1)])
    body = models.TextField(max_length=9999, validators=[MinLengthValidator(1)])
    end_time = models.DateTimeField()


    def __str__(self):
        return 'Teacher = ' + str(self.teacher) + '; class_of_course = ' + str(self.class_of_course) + \
            '; headline = ' + self.headline + '; body = ' + self.body + '; end_time = ' + \
               str(self.end_time) + '; '



class Submission(models.Model):
    student = models.ForeignKey(Student)
    submission_window = models.ForeignKey(Submission_window)
    document = models.FileField(upload_to='submission/', null=True)

    def __str__(self):
        return 'student = ' + str(self.student) + '; submission_window = ' + str(self.submission_window) + \
                '; document = ' + str(self.document) + '; '