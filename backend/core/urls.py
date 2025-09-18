from django.urls import path
from . import views

urlpatterns = [
    path('extract/', views.extract_financial_data, name='extract_financial_data'),
]
