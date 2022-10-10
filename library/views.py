from library.forms import IssueBookForm
from .forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from . import forms, models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date

def index(request):
    return render(request, "index.html")

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user,classroom=classroom,roll_no=roll_no)
        user.save()
        student.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert})
    return render(request, "student_registration.html")

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        bookid = request.POST['bookid']
        avi_copies = request.POST['copies']
        books = Book.objects.create(name=name, author=author, bookid=bookid,avilable_copies=avi_copies)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")
@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})
def allbooks(request):
    books = Book.objects.all()
    lis = []
    for i in books:
        if i.avilable_copies>0:
            t=(i.name,i.author,i.bookid,"Avilable",i.avilable_copies)
            lis.append(t)
        else:
            issuedbook=IssuedBook.objects.filter(bookid=i.bookid).order_by('expiry_date')
            t=(i.name,i.author,i.bookid,"Not Avilable",issuedbook[0].expiry_date)
            lis.append(t)
    if request.user is not None:
         if request.user.is_superuser:
            return render(request, "allbooks.html", {'books':lis,'temp':'adminnav.html'})  
         else:
            return render(request, "allbooks.html", {'books':lis,'temp':'base.html'}) 
    
@login_required(login_url = '/admin_login')    
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            student=Student.objects.get(user=request.POST['name2'])
            book=Book.objects.get(bookid=request.POST['bookid2'])
            if  student.booktaken<10 and book.avilable_copies>0:
                obj = models.IssuedBook()
                obj.student_id = request.POST['name2']
                obj.bookid=request.POST['bookid2']
                obj.save()
                student.booktaken=student.booktaken + 1
                student.save()
                book.avilable_copies=book.avilable_copies-1
                book.save()
                print("helo")
                alert = True
                return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
            return HttpResponse("Either Student have taken more than 10 books or the book is not avilable! :-Prafull")    
    return render(request, "issue_book.html", {'form':form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for issue_book in issuedBooks:
        days = (date.today()-issue_book.expiry_date)
        d=days.days
        fine=0
        if d>0:
            fine=d*5
        books = list(models.Book.objects.filter(bookid=issue_book.bookid))
        students = list(models.Student.objects.filter(user=issue_book.student_id))
        i=0
        for l in books:
            t=(students[i].user,students[i].roll_no,books[i].name,books[i].bookid,issue_book.issued_date,issue_book.expiry_date,fine,issue_book.id)
            i=i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/admin_login')
def return_book(request, myid):
    issuedBook = IssuedBook.objects.get(id=myid)
    student=Student.objects.get(user_id=issuedBook.student_id)
    book=Book.objects.get(bookid=issuedBook.bookid)
    student.booktaken=student.booktaken-1
    book.avilable_copies=book.avilable_copies+1
    student.save()
    book.save()
    issuedBook.delete()
    return redirect("/view_issued_book/")

def renew_book(request, myid):
    issuedBook = IssuedBook.objects.get(id=myid)
    if issuedBook.can_renew== True:
        issuedBook.can_renew=False
        issuedBook.expiry_date=issuedBook.expiry_date+timedelta(days=30)
        issuedBook.save()
    else:
        return HttpResponse("You have already renewed once!")
    if request.user.is_superuser:
        return redirect("/view_issued_book/")
    else :
        return redirect("/student_issued_books/")
    
@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []

    for issuebook in issuedBooks:
        book = Book.objects.get(bookid=issuebook.bookid)
        days=(date.today()-issuebook.expiry_date)
        d=days.days
        fine=0
        if d>0:
            fine=d*5
        t=(request.user.id, request.user.get_full_name, book.name,book.author,issuebook.issued_date, issuebook.expiry_date, fine,issuebook.id)
        li1.append(t)
    return render(request,'student_issued_books.html',{'li1':li1})

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert})
    return render(request, "student_login.html")

def Logout(request):
    logout(request)
    return redirect ("/")