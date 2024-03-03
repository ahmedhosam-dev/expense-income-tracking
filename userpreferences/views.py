from django.shortcuts import render
from os.path import join
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages

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
        return render(request, 'preferences/index.html', {'userName': request.user, 'currencies': currency_data, 'userPreferences': userPreferences})

    else:

        currency = request.POST['currency']
        if exists:
            userPreferences.currency = currency
            userPreferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'userName': request.user, 'currencies': currency_data, 'userPreferences': userPreferences})