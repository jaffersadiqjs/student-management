from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Auth views (simple)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('student_list')
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Students (CBVs)
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

# Courses - staff only
def staff_check(user):
    return user.is_staff

@method_decorator(user_passes_test(staff_check), name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

@method_decorator(user_passes_test(staff_check), name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

@method_decorator(user_passes_test(staff_check), name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

@method_decorator(user_passes_test(staff_check), name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

# Enroll students into courses (login required)
@login_required
def enroll_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.all()
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, f"{student.name} enrolled in {course.title}.")
        else:
            messages.info(request, f"{student.name} is already enrolled in {course.title}.")
        return redirect('student_detail', pk=student.id)
    return render(request, 'enrollment_form.html', {'student': student, 'courses': courses})

# Search students (manual HTML form)
def search_student(request):
    q = request.GET.get('q', '').strip()
    students = Student.objects.none()
    if q:
        students = Student.objects.filter(name__icontains=q) | Student.objects.filter(email__icontains=q)
    return render(request, 'search_student.html', {'students': students, 'query': q})
