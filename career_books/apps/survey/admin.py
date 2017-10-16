from django.contrib import admin

from survey.models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    raw_id_fields = ['person', ]
    readonly_fields = ['uid', 'created', 'updated', ]
    list_select_related = ('person', )
