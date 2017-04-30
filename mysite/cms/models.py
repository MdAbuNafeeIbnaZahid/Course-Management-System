from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_nom = models.IntegerField(null=True)
    email_address = models.EmailField(null=True)
    joinDate = models.DateField(null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)


class Student(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    studentId = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_nom = models.IntegerField(null=True)
    email_address = models.EmailField(null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(null=True)
    term = models.IntegerField(null=True)


class Course(models.Model):
    course_num = models.CharField(max_length=200, null=True)
    course_name = models.CharField(max_length=200, null=True)
    credi_hour = models.IntegerField(null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)


