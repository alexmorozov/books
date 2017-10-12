from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from li.models import Company, Person, Skill, IncorrectContact


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_staff_count', ]
    search_fields = ['name', ]

    def get_queryset(self, request):
        qs = super(CompanyAdmin, self).get_queryset(request)
        return qs.annotate(models.Count('staff'))

    def get_staff_count(self, obj):
        return obj.staff__count
    get_staff_count.short_description = 'Staff'
    get_staff_count.admin_order_field = 'staff__count'


class IsInvitedFilter(admin.SimpleListFilter):
    title = _('Is invited')
    parameter_name = 'is_invited'
    YES, NO = '1', '0'

    def lookups(self, request, model_admin):
        return (
            (self.YES, _('Yes')),
            (self.NO, _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == self.YES:
            return queryset.exclude(invited_at__isnull=True)
        if value == self.NO:
            return queryset.filter(invited_at__isnull=True)
        return queryset


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag', 'company', 'is_introvert', 'created',
                    'invited_at', ]
    date_hierarchy = 'invited_at'
    list_filter = [
        'is_connected',
        'is_introvert', 'tag',
        IsInvitedFilter,
    ]
    readonly_fields = ['created', 'invited_at', ]
    search_fields = ['name', ]
    select_related = ['company', ]


@admin.register(IncorrectContact)
class IncorrectContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'added_on', ]
    readonly_fields = ['added_on', ]
    search_fields = ['name', ]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
