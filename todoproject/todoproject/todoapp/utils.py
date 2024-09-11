# yourapp/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_due_date_reminder(todo):
    subject = 'Reminder: ToDo Due Date Approaching'
    message = f"Hi {todo.user.username},\n\nThis is a reminder that the ToDo item '{todo.title}' is due on {todo.due_date}.\n\nBest regards,\nYour ToDo App"
    recipient_list = [todo.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
