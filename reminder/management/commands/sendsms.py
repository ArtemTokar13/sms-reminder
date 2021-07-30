from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        from datetime import datetime

        from django.contrib.auth.models import User

        from reminder.models import Remind
        from twilio.base.exceptions import TwilioRestException
        from twilio.rest import Client

        content = Remind.objects.all()
        account_sid = "AC015c112c2b5761b3a756f528befee2c9"
        auth_token = "5da4b680602bcdb8a38c4d5a97a4f37b"
        for smscontent in content:
            if smscontent.remind_date == datetime.today().date():
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
                        print('Successfully sent message to "%s"' % recipient.username)

                    except TwilioRestException:
                        print('TwilioRestException')
        return


