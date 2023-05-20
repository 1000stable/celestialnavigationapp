from django.urls import path
from . import views


urlpatterns = [
   #path('main/', views.MainView.as_view(), name='main'),
    path('/', views.MainView.as_view(), name='main'),
    path('meridian_passage_entry/', views.Meridian_Passage_EntryView.as_view(), name='meridian_passage_entry'),
    path('latitude/', views.LatitudeView.as_view(), name='latitude'),
    path('latitude_result/', views.Latitude_ResultView.as_view(), name='latitude_result'),
    path('sunrise_sunset_entry/', views.SunriseSunsetEntryView.as_view(), name='sunrise_sunset_entry'),
    path('sunrise_sunset_result/', views.SunriseSunsetResultView.as_view(), name='sunrise_sunset_result'),
    path('sight_entry/', views.SightEntryView.as_view(), name='sight_entry'),
    path('sight_result/', views.SightResultView.as_view(), name='sight_result')
]