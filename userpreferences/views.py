from django.shortcuts import render, redirect
from os.path import join
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages
from expenses.models import Category
from income.models import Source

# Create your views here.

def index(request):
    currency_data = []
    file_path = join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for i, j in data.items():
            currency_data.append({'name': i, 'value': j})

    exists = UserPreferences.objects.filter(user=request.user).exists()
    userPreferences = None
    if exists:
        userPreferences = UserPreferences.objects.get(user=request.user)
        
    if request.method == 'GET':
        categorys = Category.objects.filter(user=request.user)
        sources = Source.objects.filter(user=request.user)

        context = {
            'userName': request.user,
            'currencies': currency_data,
            'userPreferences': userPreferences,
            'categorys': categorys,
            'sources': sources,
        }
        return render(request, 'preferences/index.html', context=context)

    else:

        currency = request.POST['currency']
        if exists:
            userPreferences.currency = currency
            userPreferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'userName': request.user, 'currencies': currency_data, 'userPreferences': userPreferences})
    

def add_category(request):
    if request.method == 'POST':
        newCategory = request.POST['category']

        if not newCategory:
            messages.warning(request, "Category name required")
            return redirect('preferences')
        
        Category.objects.create(user=request.user, name=newCategory)

        messages.success(request, "Category created")
        return redirect('preferences')

def add_source(request):
    if request.method == 'POST':
        newSource = request.POST['source']

        if not newSource:
            messages.warning(request, "Source name required")
            return redirect('preferences')
        
        Source.objects.create(user=request.user, name=newSource)

        messages.success(request, "Source created")
        return redirect('preferences')

def delete_category(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, 'Category removed')
    return redirect('preferences')



def delete_source(request, id):
    source = Source.objects.get(pk=id)
    source.delete()
    messages.success(request, 'Source removed')
    return redirect('preferences')