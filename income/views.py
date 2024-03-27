from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Source
from django.contrib import messages
from django.utils.timezone import now
from userpreferences.models import UserPreferences
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime
# Create your views here.

@login_required(login_url='/auth/login')
def index(request):
    incomes = Income.objects.all().filter(owner=request.user)
    sources = Source.objects.all().filter(user=request.user)
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency

    context = {
        'userName': request.user,
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency,
        'soursces': sources,
    }

    return render(request, 'income/index.html', context=context)

@login_required(login_url='/auth/login')
def add_income(request):
    sources = Source.objects.all().filter(user=request.user)
    context = {
        'userName': request.user,
        'sources': sources,
        'income_date': str(now().date()),
        'values': request.POST,
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount:
            messages.error(request, "Amount is required!")
            return render(request, 'income/add_income.html', context=context)
        
        if not description :
            messages.error(request, "Description is required!")
            return render(request, 'income/add_income.html', context=context)

        Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=income_date)
        messages.success(request, "Income saved successfully")
        
        return redirect('incomes')

@login_required(login_url='/auth/login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all().filter(user=request.user)
    context = {
        'income': income,
        'values': income,
        'date': str(income.date),
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']


        if not amount :
            messages.error(request, "Amount is required!")
            return render(request, 'income/add_income.html', context=context)
        
        if not description :
            messages.error(request, "Description is required!")
            return render(request, 'income/add_income.html', context=context)
        
        income.owner = request.user
        income.amount = amount
        income. date = income_date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, "Income updated successfully")

        return redirect('incomes')

@login_required(login_url='/auth/login')
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income removed")

    return redirect('incomes')

@login_required(login_url='/auth/login')
def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)

def income_source_summary(request):
    todaysDate = datetime.date.today()
    sixMonthsAgo = todaysDate - datetime.timedelta(days = 30*6)
    incomes = Income.objects.filter(owner=request.user, date__gte=sixMonthsAgo, date__lte=todaysDate)

    finalrep = {

    }

    def get_source(income):
        return income.source
    
    sourceList = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filteredBysource = incomes.filter(source=source)

        for i in filteredBysource:
            amount += i.amount
        return amount

    for x in incomes:
        for y in sourceList:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data': finalrep}, safe=False)

def summary_income(request):
    return render(request, 'income/summary_income.html')