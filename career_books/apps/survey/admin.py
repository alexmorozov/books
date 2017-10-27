from django.contrib import admin
from django.utils.html import format_html

from survey.models import Result, Book


class BooleanFilter(admin.SimpleListFilter):
    NO, YES = '0', '1'

    def lookups(self, request, model_admin):
        return (
            (self.NO, 'No'),
            (self.YES, 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == self.NO:
            return self.no(request, queryset)

        if self.value() == self.YES:
            return queryset.yes(request, queryset)


class IsFilledFilter(BooleanFilter):
    parameter_name = 'is_filled'
    title = 'Is filled out'

    def yes(self, request, queryset):
        return queryset.completed()

    def no(self, request, queryset):
        return queryset.incomplete()


class IsInvitedFilter(BooleanFilter):
    parameter_name = 'is_invited'
    title = 'Is invited'

    def yes(self, request, queryset):
        return queryset.invited()

    def no(self, request, queryset):
        return queryset.uninvited()


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    raw_id_fields = ['person', 'title1', 'title2', 'title3', ]
    readonly_fields = ['uid', 'created', 'updated', ]
    list_select_related = ('person', )
    search_fields = ['person__name', 'person__company__name', 'uid', ]
    list_filter = [IsFilledFilter, ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'gr_id', ]
    list_display = ['title', 'author', 'gr_id', 'get_image', ]

    def get_image(self, obj):
        if not obj.image:
            return ''
        return format_html('<img src="{url}" />', url=obj.image)
