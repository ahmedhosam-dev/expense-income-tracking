from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('expense_category_summary', views.expense_category_summary, name='expense_category_summary'),
    path('summary-expense', views.summary_expense, name='summary-expense'),
]