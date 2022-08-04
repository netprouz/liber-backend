import random
from ..account.models.user import User

from twilio.rest import Client as TwilioClient
from rest_framework.response import Response



account_sid = 'AC4fdab225852de8c61861a448f5e57c2d'
auth_token = "68295c2dc18dd1c1a6ba3b88c2c12196"
twilio_phone = "+19787170501"
client = TwilioClient(account_sid, auth_token)


def send_sms_code(phone_number):
    user_phone_number = User.objects.get(phone_number=phone_number).phone_number
    otp = random.randint(100000, 999999)
    user_otp = User.objects.get(phone_number=phone_number)
    user_otp.otp = otp
    user_otp.save()
    client.messages.create(
                     body="Your verification code for Liber is " + str(otp),
                     from_=twilio_phone,
                     to=user_phone_number
                 )
    return Response(status=200)


def password_reset_verification_code(phone_number):
    user_phone_number = User.objects.get(phone_number=phone_number).phone_number
    verification_code = random.randint(100000, 999999)
    user_code = User.objects.get(phone_number=phone_number)
    user_code.activating_code = verification_code
    user_code.save()
    client.messages.create(
                     body="Your verification code for Liber is " + str(verification_code),
                     from_=twilio_phone,
                     to=user_phone_number
                 )
    return Response(status=200)


