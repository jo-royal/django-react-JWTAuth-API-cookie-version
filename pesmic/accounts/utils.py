from django.core.mail import send_mail

import random
def generate_reset_code():
    return str(random.randint(100000, 999999))


def send_welcome_email(recipient_list):
    send_mail(
        subject="Welcome! we are happy to have you around",
        message="This is account confirmation, for first time, we off you a 10% OFF Discount on your total first order.. with big heart, pesmic!! ",
        from_email="noreply@example.com",
        recipient_list=[recipient_list],
        fail_silently=False,
    )


def send_password_reset_email(email, code):
    send_mail(
        subject="Password Reset Request",
        message=f"Your password reset code is: {code}",
        from_email="noreply@example.com",
        recipient_list=[email],
        fail_silently=False,
    )


