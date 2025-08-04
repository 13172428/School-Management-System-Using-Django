# myapp/management/commands/import_data.py
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from School.models import CustomUser, Student, Parent, Attendance, Result, Notification, FeePayment

class Command(BaseCommand):
    help = 'Import school data from CSV to database'

    def handle(self, *args, **options):
        with open('school_data_transformed.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # 1. Create User
                    user = CustomUser.objects.create(
                        username=row['username'],
                        password=make_password(row['password']),
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        user_type=row['user_type']
                    )
                    
                    # 2. Create Student if user is student
                    if row['user_type'] == 'student':
                        student = Student.objects.create(
                            user=user,
                            roll_number=row['roll_number'],
                            student_class=row['student_class']
                        )
                        
                        # 3. Create Parent User
                        parent_user = CustomUser.objects.create(
                            username=f"parent_{row['username']}",
                            password=make_password('parent@123'),
                            first_name=row['parent_name'].split()[0],
                            last_name='Parent',
                            email=row['parent_email'],
                            user_type='parent'
                        )
                        
                        # 4. Link Parent to Student
                        Parent.objects.create(
                            user=parent_user,
                            child=student
                        )
                        
                        # 5. Create Attendance Record
                        Attendance.objects.create(
                            student=student,
                            date=row['notification_date'],
                            subject=row['subject'],
                            status='Present' if float(row['attendance_percentage']) > 75 else 'Absent'
                        )
                        
                        # 6. Create Result
                        Result.objects.create(
                            student=student,
                            subject=row['subject'],
                            marks=row['marks'],
                            term=row['term']
                        )
                        
                        # 7. Create Fee Payment
                        FeePayment.objects.create(
                            student=student,
                            amount=5000.00 if row['fee_status'] == 'Yes' else 0.00,
                            term=row['term'],
                            date_paid=row['notification_date']
                        )
                        
                        # 8. Create Notification if exists
                        if row['notification_message']:
                            Notification.objects.create(
                                to_user=user,
                                message=row['notification_message'],
                                is_read=row['is_read']
                            )
                            
                    self.stdout.write(self.style.SUCCESS(f'Imported {row["username"]}'))
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing {row["username"]}: {str(e)}'))