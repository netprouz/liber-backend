from django.contrib.auth import get_user_model
from rest_framework import generics, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ...common import permissions
from ..serializers import user as user_serializer_
from ..utils import generate_random_password, send_password_as_sms

from ...account.sendotp import send_sms_code

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    serializer_class = user_serializer_.UserSerializer
    queryset = User.objects.all().exclude(is_staff=True, is_superuser=True)


user_list_view = UserListAPIView.as_view()


class UserGeneratePasswordAPIView(APIView):
    serializer_class = user_serializer_.UserPhoneNumberSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        password = generate_random_password()
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        phone_number = data.validated_data.get("phone_number")
        user_obj = User.objects.filter(phone_number=phone_number)
        if user_obj.exists():
            user_obj = user_obj.first()
            user_obj.set_password(password)
            user_obj.save()
        else:
            User.objects.create_user(
                phone_number=phone_number,
                password=password,
            )

        send_password_as_sms(phone_number, password)
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "your password has been sent to your phone number",
            },
        )


user_generate_password_view = UserGeneratePasswordAPIView.as_view()


class UserObtainTokenAPIView(ObtainAuthToken):
    serializer_class = user_serializer_.AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = user_serializer_.UserSerializer(instance=user)
        details = user_serializer.data
        details.update(token=token.key)
        return Response(details)


user_login_view = UserObtainTokenAPIView.as_view()


class LogoutAPIView(APIView):
    def get(self, request):
        request.user.auth_token.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"message": "You have successfully logged out"},
        )


user_logout_view = LogoutAPIView.as_view()


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter_details()
    serializer_class = user_serializer_.UserDetailSerializer
    lookup_field = "guid"


user_detail_api_view = UserDetailAPIView.as_view()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializer_.UserUpdateSerializer
    permission_classes = [permissions.UpdatePermission]
    lookup_field = "guid"


user_update_api_view = UserUpdateAPIView.as_view()


class AuthUserRegistrationView(APIView):
    serializer_class = user_serializer_.UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            send_sms_code(serializer.data['phone_number'])
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User succesfully registered',
                'user': serializer.data
            }
            return Response(response, status=status_code)

user_registration_api_view = AuthUserRegistrationView.as_view()


class AuthUserLoginView(APIView):
    serializer_class = user_serializer_.UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'phone_number': serializer.data['phone_number'],
                    # 'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

user_login_api_view = AuthUserLoginView.as_view()


class VerifyPhoneOTP(APIView):
    def post(self, request):
        data = request.data
        serializer = user_serializer_.VerifySerializer(data=data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            otp = serializer.data['otp']
            print(otp)
            user = User.objects.get(phone_number=phone_number).phone_number
            print(user)

            user_otp = User.objects.get(phone_number=phone_number)
            if user_otp.otp != otp:
                return Response({
                    'status': 400,
                    'message': 'something went worng',
                    'data': 'wrong otp'
                })
            
            user_otp.is_virified = True
            user_otp.save()

            return Response({
                    'status': 200,
                    'message': 'account virified',
                    'data': {}
                })
        return Response({
                    'status': 400,
                    'message': 'something went worng',
                    'data': serializer.errors
                })

user_otp_verify_api_view = VerifyPhoneOTP.as_view()
