from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
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

    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    address = models.CharField(max_length=200, default="", blank=True)
    phone_num = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    joinDate = models.DateField(null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    rank = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name



class Student(models.Model):

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
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, blank=True)
    studentId = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    address = models.CharField(max_length=200, default="", blank=True)
    division = models.CharField(max_length=200, null=True, choices=DIVISION, blank=True )
    phone_num = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(null=True, validators=[MinValueValidator(1),
                                           MaxValueValidator(5)])
    term = models.IntegerField(null=True, validators=[MinValueValidator(1),
                                           MaxValueValidator(2)])
    classes_enrolled_in = models.ManyToManyField( 'Class_of_course', through='Enrolment' )
    dues = models.IntegerField( default=0 )




class Course(models.Model):
    course_num = models.CharField(max_length=200, null=True)
    course_name = models.CharField(max_length=200, null=True)
    credi_hour = models.IntegerField(null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)


class Class_of_course(models.Model):
    JANUARY = 'January'
    JULY = 'July'
    SESSION_MONTH = (
        (JANUARY, 'January'),
        (JULY, 'July')
    )
    month = models.CharField(max_length=200, choices=SESSION_MONTH, null=True)
    year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2020)])
    course_of_class = models.ForeignKey(Course)
    class_teacher = models.ManyToManyField( Teacher )



########  I am skipping Department head log table. I think it is unnecessary.


#### Django doesn't need any relation table unless there are some attributes of relation...  I am skipping following tables
# Class_teacher
#
class Enrolment(models.Model):
    student = models.ForeignKey(Student)
    class_of_course = models.ForeignKey(Class_of_course)

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


