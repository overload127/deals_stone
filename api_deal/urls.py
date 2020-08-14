from django.urls import path
from . import views


app_name = 'api_deal'
urlpatterns = [
    path(
        'deals/import/csv/',
        views.DealLoadCSV.as_view(),
        name='load'
    ),
    path(
        'deals/top/<int:count>/',
        views.DealTop.as_view(),
        name='top'
    ),
]
