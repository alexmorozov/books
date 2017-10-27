# --coding: utf8--

import random
import string

import requests
import xmltodict

from django import forms
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


class BookChoiceFormField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            value = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            value = self.create_related_object(key, value)
        return value

    def create_related_object(self, key, value):
            obj, _ = self.queryset.model._default_manager.get_or_create(
                **{key: value}
            )
            return obj
            # raise ValidationError(self.error_messages['invalid_choice'],
            # code='invalid_choice')


class BookForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        final = dict(
            to='survey.Book',
            to_field='gr_id',
            db_constraint=False,
            null=True, blank=True,
        )
        final.update(kwargs)
        super(BookForeignKey, self).__init__(*args, **final)

    def deconstruct(self):
        name, path, args, kwargs = super(BookForeignKey, self).deconstruct()
        del kwargs['to_field']
        del kwargs['db_constraint']
        del kwargs['null']
        del kwargs['blank']
        del kwargs['to']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        final = dict(form_class=BookChoiceFormField)
        final.update(kwargs)
        return super(BookForeignKey, self).formfield(**final)

    def validate(self, value, model_instance):
        # Skip validation altogether, as we won't be having book objects during
        # saving
        return


class ResultQuerySet(models.QuerySet):
    def create_for(self, person):
        self.create(person=person)

    def uninvited(self):
        return self.filter(is_invited__isnull=True)

    def invited(self):
        return self.exclude(is_invited__isnull=True)

    def _completed_lookup(self):
        return (
            models.Q(title1__isnull=True) &
            models.Q(title2__isnull=True) &
            models.Q(title3__isnull=True)
        )

    def completed(self):
        return self.exclude(self._completed_lookup())

    def incomplete(self):
        return self.filter(self._completed_lookup())

    def without_followup(self):
        return self.filter(followup_sent__isnull=True)


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
    title1 = BookForeignKey(
        verbose_name='#1',
        related_name='title1')
    title2 = BookForeignKey(
        verbose_name='#2',
        related_name='title2')
    title3 = BookForeignKey(
        verbose_name='#3',
        related_name='title3')
    read_nothing = models.BooleanField(
        default=False)
    is_invited = models.DateTimeField(
        null=True, blank=True)
    followup_sent = models.DateTimeField(
        null=True, blank=True)

    objects = ResultQuerySet.as_manager()

    def __unicode__(self):
        return self.person.name

    def get_survey_url(self):
        return 'http://{host}{url}'.format(
            host=settings.ALLOWED_HOSTS[0],
            url=reverse('survey_form', args=[self.uid, ]),
        )


class Book(models.Model):
    gr_id = models.CharField(
        max_length=50, unique=True)
    title = models.CharField(
        max_length=200,
        blank=True, default='')
    author = models.CharField(
        max_length=200,
        blank=True, default='')
    image = models.URLField(
        max_length=500,
        blank=True, default='')
    amazon_url = models.URLField(
        max_length=1024,
        blank=True, default='')

    def __unicode__(self):
        return self.title or self.gr_id

    def update_from_goodreads(self):
        url = 'https://www.goodreads.com/book/show/{id}.xml?key={key}'.format(
            id=self.gr_id, key=settings.GOODREADS_API_KEY)
        response = requests.get(url)

        if response.status_code != 200:
            return

        items = xmltodict.parse(response.content)
        root = items['GoodreadsResponse']['book']

        self.title = root['title']
        self.image = root['small_image_url']
        authors = root['authors']['author']
        if not isinstance(authors, list):
            authors = [authors, ]
        self.author = authors[0]['name']

        self.save()
