from django import forms
from django.contrib.auth.models import User
from . import models

class IssueBookForm(forms.Form):
    bookid2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book [Author] [Bookid]", to_field_name="bookid", label="Book Name ")
    name2 = forms.ModelChoiceField(queryset=models.Student.objects.all(), empty_label="Name [Class] [Roll]", to_field_name="user", label="Student Details")

    bookid2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})

    
