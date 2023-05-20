from django.urls import path
from . import views


urlpatterns = [
    path('plot/', views.PlotView.as_view(), name='plot'),
]