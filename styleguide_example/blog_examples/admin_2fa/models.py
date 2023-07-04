from typing import Optional

import pyotp
import qrcode
import qrcode.image.svg
from django.conf import settings
from django.db import models


class UserTwoFactorAuthData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="two_factor_auth_data", on_delete=models.CASCADE)

    otp_secret = models.CharField(max_length=255)

    def generate_qr_code(self, name: Optional[str] = None) -> str:
        totp = pyotp.TOTP(self.otp_secret)
        qr_uri = totp.provisioning_uri(name=name, issuer_name="Styleguide Example Admin 2FA Demo")

        image_factory = qrcode.image.svg.SvgPathImage
        qr_code_image = qrcode.make(qr_uri, image_factory=image_factory)

        # The result is going to be an HTML <svg> tag
        return qr_code_image.to_string().decode("utf_8")
