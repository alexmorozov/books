# --coding: utf8--

import logging

from django.core.management import call_command, BaseCommand
from django.utils import timezone

from survey.models import Result

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--max', type=int, default=100)

    def handle(self, *args, **options):
        avail_forms = Result.objects.uninvited().order_by('pk')

        if not avail_forms.count():
            log.error('No forms available')
            return

        for form in avail_forms:
            self.send_invite(form)

    def send_invite(self, form):
        log.info('Sending an invite to %s', form.person.name)
        message = '''
Hi {{person.first_name}},

I am creating a list of the best self-development and teamwork books according to my LinkedIn contacts.
I believe that the list would be incomplete without your input.

Would you mind sharing your favorites? Here is a 1-minute form:
{url}

Once I have collected enough data, I will aggregate and publish the results.

Regards,
Alex
'''
        message = message.format(url=form.get_survey_url())
        call_command('li_send_message', form.person.pk, message)
        form.is_invited = timezone.now()
        form.save()
