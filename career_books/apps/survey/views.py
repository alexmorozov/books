from django.http import Http404
from django.http.response import JsonResponse
from django.views import generic

from dal_select2.views import Select2ViewMixin

from survey.forms import GoodReadsACForm, SurveyForm


class SurveyView(generic.FormView):
    template_name = 'survey/form.html'
    form_class = SurveyForm


class GoodReadsAutocomplete(Select2ViewMixin, generic.View):
    create_field = False

    def get(self, request, *args, **kwargs):
        form = GoodReadsACForm(self.request.GET or None)
        results = form.get_suggestions() if form.is_valid() else []
        return self.render_to_response({'object_list': results})

    def get_result_label(self, item):
        return u'<img src="{image}"> {title} ({author})'.format(**item)

    def get_result_value(self, item):
        return int(item['id'])

    def has_more(self, context):
        return False


def goodreads_autocomplete(request):
    """
    Autocomplete a book title from GoodReads.
    """
    form = GoodReadsACForm(request.GET or None)
    if not form.is_valid():
        raise Http404
    return JsonResponse(
        dict(suggestions=form.get_suggestions())
    )
