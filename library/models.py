from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    bookid = models.CharField(max_length=5,unique=True)
    avilable_copies=models.PositiveSmallIntegerField(default=5)

    def __str__(self):
       return str(self.name) +" ["+str(self.author)+']'+ " ["+str(self.bookid)+']'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3,unique=True)
    booktaken = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.user) + "  ["+str(self.classroom)+'] ' + " ["+str(self.roll_no)+']'



def expiry():
    return datetime.today() + timedelta(days=30)

class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True) 
    bookid = models.CharField(max_length=5)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    can_renew=models.BooleanField(default=True)