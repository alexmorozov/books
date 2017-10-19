from django.contrib import admin
from django.utils.html import format_html

from survey.models import Result, Book


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    raw_id_fields = ['person', 'title1', 'title2', 'title3', ]
    readonly_fields = ['uid', 'created', 'updated', ]
    list_select_related = ('person', )
    search_fields = ['person__name', 'person__company__name', ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'gr_id', ]
    list_display = ['title', 'author', 'gr_id', 'get_image', ]

    def get_image(self, obj):
        if not obj.image:
            return ''
        return format_html('<img src="{url}" />', url=obj.image)
