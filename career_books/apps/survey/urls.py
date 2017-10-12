from django.conf.urls import url

from survey import views

urlpatterns = [
    url(r'^autocomplete$', views.GoodReadsAutocomplete.as_view(),
        name='survey_book_autocomplete'),
    url(r'^$', views.SurveyView.as_view(),
        name='survey_form'),
]
