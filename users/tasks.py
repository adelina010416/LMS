from datetime import datetime

from celery import shared_task

from users.models import User


@shared_task
def check_user_last_login():
    users = User.objects.all()
    for user in users:
        time_absence = datetime.now() - user.last_login
        if time_absence.days > 31:
            user.is_active = False
            user.save()
