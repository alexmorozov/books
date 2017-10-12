from django.conf.urls import url

from survey import views

urlpatterns = [
    url(r'^autocomplete$', views.GoodReadsAutocomplete.as_view(),
        name='survey_book_autocomplete'),
    url(r'^(?P<uid>[a-z0-9]+)$', views.SurveyView.as_view(),
        name='survey_form'),
    url(r'^(?P<uid>[a-z0-9]+)/thanks$', views.SurveyThanks.as_view(),
        name='survey_thanks'),
]
