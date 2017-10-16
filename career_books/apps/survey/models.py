# --coding: utf8--

import random
import string

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


class Result(models.Model):
    person = models.ForeignKey(
        Person)
    created = models.DateTimeField(
        auto_now_add=True)
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

    def __unicode__(self):
        return self.person.name


class Invite(models.Model):
    person = models.ForeignKey(
        Person, related_name='invites')
    form = models.ForeignKey(
        Result, related_name='invites')
    created = models.DateTimeField(
        auto_now_add=True)
