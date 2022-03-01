from celery import shared_task
from users.models import User


@shared_task
def send_user_email(user_id, template_id, context={}):
    pass
