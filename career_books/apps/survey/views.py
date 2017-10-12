from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import JsonResponse
from django.views import generic

from dal_select2.views import Select2ViewMixin

from survey.forms import GoodReadsACForm, SurveyForm
from survey.models import Result


class SurveyView(generic.UpdateView):
    template_name = 'survey/form.html'
    model = Result
    form_class = SurveyForm
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def get_success_url(self):
        return reverse('survey_thanks', kwargs={'uid': self.object.uid})


class SurveyThanks(generic.DetailView):
    template_name = 'survey/thanks.html'
    model = Result
    slug_url_kwarg = 'uid'
    slug_field = 'uid'


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
