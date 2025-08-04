from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin','Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


# -------------------------
# Student Model
# -------------------------
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, default='0000')  # Default added
    student_class = models.CharField(max_length=20, default='Class A')  # Default added

    def __str__(self):
        return self.user.username


# -------------------------
# Parent Model
# -------------------------
class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    child = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# -------------------------
# Teacher Model
# -------------------------
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, default='Math')  # Add your actual default
    assigned_class = models.CharField(max_length=20, default='Class A')

    def __str__(self):
        return self.user.username

                         


# -------------------------
# Attendance Model
# -------------------------
class Attendance(models.Model):
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"


# -------------------------
# Result Model
# -------------------------
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    term = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject}"


# -------------------------
# Notification Model
# -------------------------
class Notification(models.Model):
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To: {self.to_user.username}"
# Add this to your models.py
class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    term = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.user.username} - ₹{self.amount} - {self.term}"
class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

