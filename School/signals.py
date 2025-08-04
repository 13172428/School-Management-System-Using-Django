# School/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance, Result, Notification

@receiver(post_save, sender=Attendance)
def notify_parent_attendance(sender, instance, created, **kwargs):
    if created and not instance.status:
        parent_user = getattr(instance.student.parent, 'user', None)
        if parent_user:
            Notification.objects.create(
                to_user=parent_user,
                message=f'{instance.student.user.get_full_name()} was absent in {instance.subject.name} on {instance.date}.'
            )

@receiver(post_save, sender=Result)
def notify_parent_result(sender, instance, created, **kwargs):
    if created:
        parent_user = getattr(instance.student.parent, 'user', None)
        if parent_user:
            Notification.objects.create(
                to_user=parent_user,
                message=f'New mark in {instance.subject.name}: {instance.marks}%'
            )
