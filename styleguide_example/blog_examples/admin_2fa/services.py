import pyotp
from django.core.exceptions import ValidationError

from styleguide_example.users.models import BaseUser

from .models import UserTwoFactorAuthData


def user_two_factor_auth_data_create(*, user: BaseUser) -> UserTwoFactorAuthData:
    if hasattr(user, "two_factor_auth_data"):
        raise ValidationError("Can not have more than one 2FA related data.")

    two_factor_auth_data = UserTwoFactorAuthData.objects.create(user=user, otp_secret=pyotp.random_base32())

    return two_factor_auth_data
