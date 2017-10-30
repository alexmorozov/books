# --coding: utf8--

from datetime import timedelta
import logging

from django.core.management import call_command, BaseCommand
from django.utils import timezone

from survey.models import Result

log = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--max', type=int, default=100)
        parser.add_argument('--days', type=int, default=5)
        parser.add_argument('--dry-run', type=bool, default=False)

    def handle(self, *args, **options):
        incomplete = Result.objects.invited().incomplete().without_followup()

        threshold = timezone.now().date() - timedelta(days=options['days'])
        outstanding = incomplete.filter(is_invited__date__lte=threshold)

        if not outstanding.count():
            log.error('No outstanding invites')
            return

        for form in outstanding:
            self.send_followup(form, dry_run=options['dry_run'])

    def send_followup(self, form, dry_run=False):
        log.info('Sending a followup to %s', form.person.name)
        message = '''
Hi {{person.first_name}},

Did you have a chance to look at my survey form?
Let me remind you what the point is.

I want to create a super-useful list of greatest books on self-development and teamwork.
But I'd like to ask out not theorists and professional critics, but successful
practitioners like you.

That's why I need your input very much. It would take just a minute.
Here's the link to the form: {url}
If you don't read that kind of books, plese check the corresponding checkbox, that's a very valueable input too.

If there are any issues with filling out the form, just let me know.
I'll get that straightened out right away.

Regards,
Alex
'''
        message = message.format(url=form.get_survey_url())
        call_command('li_send_message', form.person.pk, message,
                     dry_run=dry_run)
        form.followup_sent = timezone.now()
        form.save()
