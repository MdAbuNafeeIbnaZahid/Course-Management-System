from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    username = models.CharField(unique=True)
    password = models.CharField(widget=forms.Pass)




