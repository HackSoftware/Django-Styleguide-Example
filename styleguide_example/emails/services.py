import random

from django.db import transaction
from django.db.models.query import QuerySet
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings

from styleguide_example.core.exceptions import ApplicationError

from styleguide_example.common.services import model_update

from styleguide_example.emails.models import Email
from styleguide_example.emails.tasks import email_send as email_send_task


@transaction.atomic
def email_failed(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot fail non-sending emails. Current status is {email.status}")

    email, _ = model_update(
        instance=email,
        fields=["status"],
        data={
            "status": Email.Status.FAILED
        }
    )
    return email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    if settings.EMAIL_SENDING_FAILURE_TRIGGER:
        failure_dice = random.uniform(0, 1)

        if failure_dice <= settings.EMAIL_SENDING_FAILURE_RATE:
            raise ApplicationError("Email sending failure triggered.")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            "sent_at": timezone.now()
        }
    )
    return email


def email_send_all(emails: QuerySet[Email]):
    """
    This is a very specific service.

    We don't want to decorate with @transaction.atomic,
    since we are executing updates, 1 by 1, in a separate atomic block,
    so we can trigger transaction.on_commit for each email, separately.
    """
    for email in emails:
        with transaction.atomic():
            Email.objects.filter(id=email.id).update(
                status=Email.Status.SENDING
            )

        # Create a closure, to capture the proper value of each id
        transaction.on_commit(
            (
                lambda email_id: lambda: email_send_task.delay(email_id)
            )(email.id)
        )
