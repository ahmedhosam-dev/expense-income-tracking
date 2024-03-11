from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='incomes'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.edit_income, name='edit-income'),
    path('delete-income/<int:id>', views.delete_income, name='delete-income'),
    path('search-incomes', csrf_exempt(views.search_incomes), name="search-incomes"),
    path('income_source_summary', views.income_source_summary, name='income_source_summary'),
    path('summary_income', views.summary_income, name='summary-income')
]