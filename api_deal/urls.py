from django.urls import path
from . import views


app_name = 'api_deal'
urlpatterns = [
    path(
        'test/',
        views.TestView.as_view(),
        name='test'
    ),
]