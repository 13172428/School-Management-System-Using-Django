# School/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import CustomUser, Attendance, Result, FeePayment, Notification, Subject
from django.db.models import Count, Sum, Q

def home(request):
    return render(request, 'html/index.html')

def post_login_redirect(user):
    if user.user_type == 'student':
        return 'student_dashboard'
    if user.user_type == 'teacher':
        return 'teacher_dashboard'
    if user.user_type == 'parent':
        return 'parent_dashboard'
    return 'index'

def unified_login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=username_or_email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect(post_login_redirect(user))
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'html/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------
# Dashboard Views
# -----------------------

class StudentDashboard(TemplateView):
    template_name = 'html/student.html'

    def get_context_data(self, **kw):
        student = self.request.user.student
        ctx = super().get_context_data(**kw)

        att_qs = Attendance.objects.filter(student=student)
        total = att_qs.count()
        present = att_qs.filter(status='Present').count()

        ctx['attendance_percent'] = round((present / total) * 100, 1) if total else 0
        ctx['by_subject'] = att_qs.values('subject').annotate(
            present=Count('id', filter=Q(status='Present')),
            total=Count('id')
        )
        ctx['latest_marks'] = Result.objects.filter(student=student).order_by('-term')[:6]
        ctx['fees_paid'] = FeePayment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        ctx['notifications'] = Notification.objects.filter(to_user=self.request.user, is_read=False)[:5]
        return ctx

class ParentDashboard(TemplateView):
    template_name = 'html/parent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            parent = self.request.user.parent
            student = parent.child  # Linked student
        except Exception as e:
            context['error'] = f"Error: No child linked to this parent or data is invalid."
            return context

        att_qs = Attendance.objects.filter(student=student)
        total = att_qs.count()
        present = att_qs.filter(status='Present').count()

        attendance_percent = round((present / total) * 100, 1) if total else 0
        fees_paid = FeePayment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        marks = Result.objects.filter(student=student).order_by('-term')[:10]

        context.update({
            'child': student,
            'attendance_percent': attendance_percent,
            'fees_paid': fees_paid,
            'marks': marks,
            'notifications': Notification.objects.filter(to_user=self.request.user, is_read=False)[:5],
        })
        return context

class TeacherDashboard(TemplateView):
    template_name = 'html/teacher.html'

    def get_context_data(self, **kw):
        teacher = self.request.user.teacher
        ctx = super().get_context_data(**kw)

        subjects = Subject.objects.filter(teacher=teacher)
        ctx['subjects'] = subjects
        ctx['total_classes'] = subjects.count()
        ctx['class_subjects'] = subjects
        ctx['notifications'] = Notification.objects.filter(to_user=self.request.user, is_read=False)[:5]
        return ctx
