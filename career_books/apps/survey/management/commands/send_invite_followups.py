# --coding: utf8--

from datetime import timedelta
import logging

from django.utils import timezone

from whws.management.commands.base import ProcessListCommand
from whws.linkedin import send_message

from survey.models import Result

log = logging.getLogger(__name__)


class Command(ProcessListCommand):
    def add_arguments(self, parser):
        parser.add_argument('--max', type=int, default=100)
        parser.add_argument('--days', type=int, default=5)
        parser.add_argument('--dry-run', action='store_true')

    def get_list(self, *args, **options):
        incomplete = Result.objects.invited().incomplete().without_followup()

        threshold = timezone.now().date() - timedelta(days=options['days'])
        outstanding = incomplete.filter(is_invited__date__lte=threshold)

        return outstanding

    def process_item(self, item, *args, **options):
        log.info('Sending a followup to %s', item.person.name)
        message = '''
Hi {person.first_name},

Did you have a chance to look at my survey form?
Let me remind you what the point is.

I want to create a super-useful list of greatest books on business, self-development and teamwork.
But I'd like to ask out not theorists and professional critics, but successful
practitioners like you.

That's why I need your input very much. It would take just a minute.
Here's the link to the form: {url}
If you don't read that kind of books, please check the corresponding checkbox, that's a valuable input too.

If there are any issues with filling out the form, just let me know.
I'll get that straightened out right away.

Regards,
Alex
'''
        message = message.format(url=item.get_survey_url(),
                                 person=item.person).strip()
        send_message(self.browser, item.person.profile_url,
                     message, dry_run=options['dry_run'])

    def finalize_item(self, item, results, *args, **options):
        if not options['dry_run']:
            item.followup_sent = timezone.now()
            item.save()

    def skip_item(self, item, *args, **options):
        if not options['dry_run']:
            item.followup_sent = timezone.now()
            item.read_nothing = True
            item.save()
