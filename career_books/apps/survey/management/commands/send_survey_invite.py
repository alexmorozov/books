# --coding: utf8--

import logging

from django.conf import settings
from django.utils import timezone

from whws.management.commands.base import BaseBrowserCommand
from li.models import Person

log = logging.getLogger(__name__)


class Command(BaseBrowserCommand):
    def add_arguments(self, parser):
        parser.add_argument('person_pk', type=str)

    def handle(self, *args, **options):
        log.info('Sending an invite to %s', person.name)
        call_command('li_send_message', options['person_pk'],
                     options['message'])
