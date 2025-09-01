from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Students
    path('', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('student/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    # Courses (staff only)
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('course/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # Enrollment & Search
    path('enroll/<int:student_id>/', views.enroll_student, name='enroll_student'),
    path('search/', views.search_student, name='search_student'),
]
