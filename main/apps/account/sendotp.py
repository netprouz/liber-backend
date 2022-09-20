import random
from ..account.models.user import User

from twilio.rest import Client as TwilioClient
from rest_framework.response import Response

from django.core.mail import EmailMessage
from django.conf import settings



account_sid = 'AC59d0629692bb9a29e294b73663696933'
auth_token = "9a1035b65c166d343605b2697a80b10b"
twilio_phone = "+18329798435"
client = TwilioClient(account_sid, auth_token)


def send_sms_code(username):
    user_phone_number = User.objects.get(username=username).username
    otp = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    user_otp.otp = otp
    user_otp.save()
    client.messages.create(
                     body="Your verification code for Liber is " + str(otp),
                     from_=twilio_phone,
                     to=user_phone_number
                 )
    return Response(status=200)


def password_reset_verification_code_by_phone_number(username):
    username = User.objects.get(username=username).username
    verification_code = random.randint(100000, 999999)
    user_code = User.objects.get(username=username)
    user_code.activating_code = verification_code
    user_code.save()
    client.messages.create(
                     body="Your verification code for Liber is " + str(verification_code),
                     from_=twilio_phone,
                     to=username
                 )
    return Response(status=200)


def send_otp_to_email(username):
    user_email = User.objects.get(username=username).username
    otp = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    user_otp.otp = otp
    user_otp.save()

    email = EmailMessage(
                        "Your verification code for Liber is " + str(otp),
                        settings.EMAIL_HOST_USER,
                        to=[user_email]
    )
    email.send()
    
    return Response(status=200)


def password_reset_verification_code_by_email(username):
    user_email = User.objects.get(username=username).username
    verification_code = random.randint(100000, 999999)
    user_otp = User.objects.get(username=username)
    user_otp.activating_code = verification_code
    user_otp.save()

    email = EmailMessage(
                        "Your verification code for Liber is " + str(verification_code),
                        settings.EMAIL_HOST_USER,
                        to=[user_email]
    )
    email.send()
    
    return Response(status=200)




