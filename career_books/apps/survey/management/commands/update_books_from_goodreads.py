# --coding: utf8--

import logging
import time

from django.core.management import BaseCommand

from survey.models import Book

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help_text = 'Update book data from GoodReads'

    def handle(self, *args, **options):
        books = Book.objects.filter(title='')
        total = 0
        for book in books:
            book.update_from_goodreads()
            time.sleep(0.5)
            total += 1

        self.stdout.write('Updated {0} book(s)'.format(total))
