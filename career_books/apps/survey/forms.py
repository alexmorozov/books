# --coding: utf8--

import requests
import xmltodict

from django.conf import settings
from django import forms

from dal import autocomplete

from survey.models import Result


class GoodReadsACForm(forms.Form):
    AC_URL = 'https://www.goodreads.com/search/index.xml?q={query}&key={key}'

    q = forms.CharField()

    def get_suggestions(self):
        assert self.is_valid()
        suggestions = []

        url = self.AC_URL.format(query=self.cleaned_data['q'],
                                 key=settings.GOODREADS_API_KEY)
        response = requests.get(url)
        if response.status_code != 200:
            return suggestions

        items = xmltodict.parse(response.content)

        total = int(items
                    .get('GoodreadsResponse', {})
                    .get('search', {})
                    .get('total-results', 0))
        if not total:
            return suggestions

        results = items['GoodreadsResponse']['search']['results']['work']

        if not isinstance(results, list):
            # Just one result
            results = [results, ]

        for result in results:
            book = result['best_book']
            suggestions.append(
                dict(
                    id=book['id']['#text'],
                    title=book['title'],
                    author=book['author']['name'],
                    image=book['small_image_url']
                )
            )

        return suggestions


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Result
        ac_widget = autocomplete.Select2(
            url='survey_book_autocomplete',
            attrs={
                'data-html': True,
                'data-placeholder': 'Click here and start typing the title.',
            }
        )
        fields = ['title1', 'title2', 'title3', 'read_nothing', ]
        widgets = {
            'title1': ac_widget,
            'title2': ac_widget,
            'title3': ac_widget,
        }

    def clean(self):
        cleaned_data = super(SurveyForm, self).clean()
        titles = any(cleaned_data.get(title)
                     for title in ['title1', 'title2', 'title3', ])

        if not titles and not cleaned_data.get('read_nothing'):
            raise forms.ValidationError('Please either specify at least one '
                                        'title or set the checkbox below')
