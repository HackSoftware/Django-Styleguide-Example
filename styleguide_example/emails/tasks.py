from celery import shared_task

from styleguide_example.emails.models import Email


@shared_task
def email_send(email_id):
    # TODO: Add error handling
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send
    email_send(email)
