from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("student_registration/", views.student_registration, name="student_registration"),
    path("add_book/", views.add_book, name="add_book"),
    path("allbooks/", views.allbooks, name="allbooks"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("return_book/<int:myid>/", views.return_book, name="return_book"),
    path("renew_book/<int:myid>/", views.renew_book, name="renew_book"),
    path("student_login/", views.student_login, name="student_login"),
    path("profile/", views.profile, name="profile"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),
]