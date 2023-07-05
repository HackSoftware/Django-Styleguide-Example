from django.core.exceptions import ValidationError
from django.views.generic import TemplateView

from .services import user_two_factor_auth_data_create


class AdminSetupTwoFactorAuthView(TemplateView):
    template_name = "admin_2fa/setup_2fa.html"

    def post(self, request):
        context = {}
        user = request.user

        try:
            two_factor_auth_data = user_two_factor_auth_data_create(user=user)
            otp_secret = two_factor_auth_data.otp_secret

            context["otp_secret"] = otp_secret
            context["qr_code"] = two_factor_auth_data.generate_qr_code(name=user.email)
        except ValidationError as exc:
            context["form_errors"] = exc.messages

        return self.render_to_response(context)
