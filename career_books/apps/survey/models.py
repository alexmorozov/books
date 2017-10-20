# --coding: utf8--

import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


from li.models import Person


def new_uid():
    while True:
        uid = ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for _ in range(6)
        )
        if not Result.objects.filter(uid=uid).exists():
            return uid


class ResultQuerySet(models.QuerySet):
    def create_for(self, person):
        self.create(person=person)

    def uninvited(self):
        return self.filter(is_invited__isnull=True)


class Result(models.Model):
    person = models.ForeignKey(
        Person, related_name='forms')
    created = models.DateTimeField(
        auto_now_add=True)
    updated = models.DateTimeField(
        auto_now=True)
    uid = models.CharField(
        max_length=10, unique=True, editable=False,
        default=new_uid)
    title1 = models.CharField(
        verbose_name='#1', default='',
        max_length=50, blank=True)
    title2 = models.CharField(
        verbose_name='#2', default='',
        max_length=50, blank=True)
    title3 = models.CharField(
        verbose_name='#3', default='',
        max_length=50, blank=True)
    is_invited = models.DateTimeField(
        null=True, blank=True)

    objects = ResultQuerySet.as_manager()

    def __unicode__(self):
        return self.person.name

    def get_survey_url(self):
        return 'http://{host}{url}'.format(
            host=settings.ALLOWED_HOSTS[0],
            url=reverse('survey_form', args=[self.uid, ]),
        )
