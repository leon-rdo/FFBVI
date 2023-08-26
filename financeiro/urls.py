from django.urls import path
from .views import *

app_name = 'financeiro'
urlpatterns = [
    path('', IndexView.as_view(), name='menu_financeiro'),
]

