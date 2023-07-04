import pyotp
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import UserTwoFactorAuthData

User = get_user_model()


def user_two_factor_auth_data_create(*, user: User) -> UserTwoFactorAuthData:
    if hasattr(user, "two_factor_auth_data"):
        raise ValidationError("Can not have more than one 2FA related data.")

    two_factor_auth_data = UserTwoFactorAuthData.objects.create(user=user, otp_secret=pyotp.random_base32())

    return two_factor_auth_data
