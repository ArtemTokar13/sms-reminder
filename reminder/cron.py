import datetime
from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User

from reminder.models import Remind
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


def my_scheduled_job():
    content = Remind.objects.all()
    account_sid = "AC015c112c2b5761b3a756f528befee2c9"
    auth_token = "a146165a8ac791c156d05d4033838842"
    for smscontent in content:
        if smscontent.remind_date == datetime.today().date():
            if ((datetime.now() + timedelta(minutes=1)).time()) < smscontent.remind_time < ((datetime.now() + timedelta(minutes=5)).time()):
                tempusers = User.objects.filter(username=smscontent.author)
                for recipient in tempusers:
                    try:
                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                            body="I just want to remind, that you have some task for today {date}: {task}. {time} is the deadline!".format(
                                date=str(smscontent.remind_date), task=str(smscontent.title),
                                time=str(smscontent.remind_time)),
                            to=str(recipient.username),
                            from_="+18568889437")
                        print(message.sid)

                    except TwilioRestException:
                        pass
    return


