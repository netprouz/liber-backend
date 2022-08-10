from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ..models.user import User
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "guid",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
        )


class UserPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        self._errors = {}
        phone_number = attrs.get("phone_number")
        if len(phone_number) != 12:
            self._errors[
                "invalid_format"
            ] = "Phone number should contain 12 digits. Format: 998xxxxxxxxx "
        if not phone_number.isdigit():
            self._errors[
                "invalid_number"
            ] = "Phone number should consist of only digits. Format: 998xxxxxxxxx "  # noqa

        if self.errors:
            raise serializers.ValidationError(self._errors)
        return attrs


class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label=_("Phone number"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )

    def validate(self, attrs):
        self._errors = {}
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        if len(phone_number) != 12:
            self._errors[
                "invalid_format"
            ] = "Phone number should contain 12 digits. Format: 998xxxxxxxxx "
        if not phone_number.isdigit():
            self._errors[
                "invalid_number"
            ] = "Phone number should consist of only digits. Format: 998xxxxxxxxx "  # noqa

        if not phone_number or not password:
            self._errors[
                "invalid_credentials"
            ] = "Phone number and password are required"

        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            self._errors[
                "authentication_failed"
            ] = "The current user has either been blocked or inactive"

        if self._errors:
            raise serializers.ValidationError(self._errors)

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class UserOrderSerializer(serializers.Serializer):
    payment_type = serializers.CharField()
    book = serializers.SlugField()
    phone_number = serializers.CharField()
    full_name = serializers.CharField()
    is_paid = serializers.BooleanField()
    is_completed = serializers.BooleanField()
    order_number = serializers.CharField()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2)


class UserTranscationSerializer(serializers.Serializer):
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    transaction_external_id = serializers.CharField()
    is_verified = serializers.BooleanField()
    is_paid = serializers.BooleanField()
    is_canceled = serializers.BooleanField()
    transaction_type = serializers.CharField()
    status = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=20, decimal_places=2, allow_null=True)
    orders = UserOrderSerializer(many=True, allow_null=True, required=False)
    transactions = UserTranscationSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "balance",
            "orders",
            "transactions",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "guid",
            "first_name",
            "last_name",
            "profile_picture",
            "gender",
            "date_of_birth",
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password'
        )    

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # email = user.email
        # if email:
        #     token['email'] = user.email
        #     return token
        # phone_number = user.phone_number
        # if phone_number:
        token['username'] = user.username
        return token



class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        phone_number = data['phone_number']
        password = data['password']
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'phone_number': user.phone_number,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class VerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()    

    def validate(self, attrs):
        self._errors = {}
        username = attrs.get('username')
        # user = User.objects.filter(username=username).exists()
     
        if not '+998' in username or not '@' in username:
            self._errors[
                'Invalid format'
            ] = 'Enter correct format'
        # elif not '@' in username:
        #     self._errors[
        #         'Invalid format'
        #     ] = 'Enter correct format'
        if self.errors:
            raise serializers.ValidationError(self._errors)
        return attrs

    def create(self, validated_date):
        return validated_date
    


    # def validate(self, attrs):
    #     self._errors = {}
    #     phone_number = attrs.get("phone_number")
    #     if len(phone_number) != 13:
    #         self._errors[
    #             "invalid_format"
    #         ] = "Phone number should contain 12 digits. Format: 998xxxxxxxxx "
    #     if self.errors:
    #         raise serializers.ValidationError(self._errors)
    #     return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()


class PasswordResetCodeCheckSerializer(serializers.Serializer):
    confirm_code = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    # username = serializers.CharField()
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': _('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail(_('bad_token'))
