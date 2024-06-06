from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer
from allauth.account.models import EmailAddress
from books.serializers import BookSerializer

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.nickname = self.data.get("nickname")
        user.save()
        return user


class CustomUserDetailSerializer(UserDetailsSerializer):
    email = serializers.EmailField(read_only=True)
    # books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
        )


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                msg = _("이메일 또는 비밀번호가 잘못되었습니다.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("이메일과 비밀번호를 모두 입력해주세요.")
            raise serializers.ValidationError(msg, code="authorization")

        user = authenticate(email=email, password=password)
        if user:
            email_address = EmailAddress.objects.filter(
                user=user, verified=True
            ).exists()
            if not email_address:
                raise serializers.ValidationError("Email is not verified.")
        else:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        attrs["user"] = user
        return attrs

    class Meta:
        fields = (
            "email",
            "password",
        )


class ProfileSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "books",
        )
