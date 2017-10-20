# --coding: utf8--

import logging

from django.core.management import BaseCommand
from django.db.models import Count

from li.models import Person
from survey.models import Result

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help_text = 'Create missing survey forms'

    def handle(self, *args, **options):
        avail = (Person.objects
                 .annotate(Count('forms'))
                 .filter(is_connected=True, forms__count=0))
        total = 0
        for person in avail:
            Result.objects.create_for(person)
            total += 1

        self.stdout.write('Created {0} form(s)'.format(total))
