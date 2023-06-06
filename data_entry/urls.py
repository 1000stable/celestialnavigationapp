from django.urls import path
from . import views


urlpatterns = [
    #path('main/', views.MainView.as_view(), name='main'),
    path('', views.MainView.as_view(), name='main'),
    path('meridian_passage_entry/', views.Meridian_Passage_EntryView.as_view(), name='meridian_passage_entry'),
    path('latitude_entry/', views.LatitudeView.as_view(), name='latitude_entry'),
    path('latitude_result/', views.Latitude_ResultView.as_view(), name='latitude_result'),
    path('sunrise_sunset_entry/', views.SunriseSunsetEntryView.as_view(), name='sunrise_sunset_entry'),
    path('sunrise_sunset_result/', views.SunriseSunsetResultView.as_view(), name='sunrise_sunset_result'),
    path('sight_entry/', views.SightEntryView.as_view(), name='sight_entry'),
    path('sight_almanac_entry/', views.SightAlmanacEntryView.as_view(), name='sight_almanac_entry'),
    path('sight_result/', views.SightResultView.as_view(), name='sight_result'),
    path('star_finder_time_entry/', views.StarFinderTimeEntryView.as_view(), name='star_finder_time_entry'),
    path('star_finder_gha_aries_entry/', views.StarFinderGhaAriesEntryView.as_view(), name='star_finder_gha_aries_entry'),
    path('star_finder_lha_aries_result/', views.StarFinderLhaAriesResultView.as_view(), name='star_finder_lha_aries_result')
] 