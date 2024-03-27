from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='preferences'),
    path('add-category', views.add_category, name='add-category'),
    path('add-source', views.add_source, name='add-source'),
    path('delete-category/<int:id>', views.delete_category, name='delete-category'),
    path('delete-source/<int:id>', views.delete_source, name='delete-source'),
]