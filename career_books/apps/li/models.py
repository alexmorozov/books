from __future__ import unicode_literals

from django.db import models

from li.utils import canonicalize


class Company(models.Model):
    name = models.CharField(
        max_length=1000)
    location = models.CharField(
        max_length=100,
        blank=True, default='')
    industry = models.CharField(
        max_length=1000,
        blank=True, default='')
    website = models.URLField(
        max_length=1000,
        blank=True, default='')
    year_founded = models.IntegerField(
        blank=True, null=True)
    company_type = models.CharField(
        max_length=200,
        blank=True, default='')
    employee_count = models.IntegerField(
        default=0)

    class Meta:
        db_table = 'company'
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name


class PersonQuerySet(models.QuerySet):
    def uninvited(self, tag, limit=None):
        """
        Return list of uninvited persons by given tag.
        """
        queryset = (self
                    .filter(tag=tag)
                    .filter(is_introvert=False)
                    .filter(invited_at__isnull=True)
                    .order_by('created'))
        if limit:
            queryset = queryset[:limit]

        return queryset

    def from_distinct_companies(self):
        """
        One person for each company.
        """
        return (self
                .exclude(company_isnull=True)
                .distinct('company'))

    def random(self, limit=None):
        query = self.order_by('?')
        if limit:
            query = query[:limit]
        return query


class Person(models.Model):
    name = models.CharField(
        max_length=1000)
    tag = models.CharField(
        max_length=255)
    profile_url = models.URLField(
        unique=True, max_length=1024)

    created = models.DateTimeField(
        auto_now_add=True)
    invited_at = models.DateTimeField(
        null=True, blank=True)
    is_connected = models.BooleanField(
        default=False)
    is_introvert = models.BooleanField(
        default=False)
    connected_at = models.DateTimeField(
        null=True, blank=True)

    region = models.CharField(
        blank=True, default='',
        max_length=400)
    company = models.ForeignKey(
        Company, null=True, blank=True,
        related_name='staff')
    position = models.CharField(
        blank=True, default='',
        max_length=400)

    email = models.EmailField(
        blank=True, default='',
        max_length=100)

    skills = models.ManyToManyField(
        'Skill',
        blank=True)

    objects = PersonQuerySet.as_manager()

    class Meta:
        db_table = 'person'
        verbose_name_plural = 'people'

    def __unicode__(self):
        if self.company:
            return u'{o.name} ({o.company})'.format(o=self)
        return self.name

    @property
    def first_name(self):
        return self.name.split()[0]

    def save(self, **kwargs):
        self.profile_url = canonicalize(self.profile_url)
        super(Person, self).save(**kwargs)


class IncorrectContact(models.Model):
    """
    A contact we've been unable to find on Linkedin.
    """
    name = models.CharField(
        max_length=500, unique=True)
    added_on = models.DateTimeField(
        auto_now_add=True)

    def __unicode__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(
        max_length=300, unique=True)

    def __unicode__(self):
        return self.name
