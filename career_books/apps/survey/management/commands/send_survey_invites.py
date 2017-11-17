# --coding: utf8--

import logging

from whws.management.commands.base import ProcessListCommand
from whws.linkedin import send_message

from django.utils import timezone

from survey.models import Result

log = logging.getLogger(__name__)


class Command(ProcessListCommand):
    def add_arguments(self, parser):
        parser.add_argument('--max', type=int, default=100)
        parser.add_argument('--dry-run', action='store_true')

    def get_list(self, *args, **options):
        return (Result.objects
                .uninvited()
                .order_by('pk')
                [:options['max']])

    def process_item(self, item, *args, **options):
        log.info('Sending an invite to %s', item.person.name)
        message = u'''
Hi {person.first_name},

I am creating a list of the best business, self-development, leadership, and teamwork books according to my LinkedIn contacts.
Would you mind sharing your favorites? Here is a 1-minute form:
{url}

Once I have collected enough data, I will aggregate and publish the results.
Let's create the best list ever!

Regards,
Alex
'''
        message = message.format(url=item.get_survey_url(),
                                 person=item.person).strip()
        send_message(self.browser, item.person.profile_url,
                     message, dry_run=options['dry_run'])

    def finalize_item(self, item, results, *args, **options):
        if not options['dry_run']:
            item.is_invited = timezone.now()
            item.save()

    def skip_item(self, item, *args, **options):
        if not options['dry_run']:
            item.is_invited = timezone.now()
            item.read_nothing = True
            item.save()
