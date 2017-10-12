# --coding: utf8--

import requests
import xmltodict

from django.conf import settings
from django import forms

from dal import autocomplete


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


class SurveyForm(forms.Form):
    title1 = forms.CharField(
        widget=autocomplete.Select2(url='survey_book_autocomplete',
                                    attrs={'data-html': True,
                                           'data-placeholder': 'Choose...'
                                           })
    )
