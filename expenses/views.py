from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
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
    expenses = Expense.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency

    context = {
        'userName': request.user,
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'categories': categories,
    }

    return render(request, 'expenses/index.html', context=context)

@login_required(login_url='/auth/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'userName': request.user,
        'categories': categories,
        'expense_date': str(now().date()),
        'values': request.POST,
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context=context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        if not amount:
            messages.error(request, "Amount is required!")
            return render(request, 'expenses/add_expense.html', context=context)

        if not description :
            messages.error(request, "Description is required!")
            return render(request, 'expenses/add_expense.html', context=context)

        Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=expense_date)
        messages.success(request, "Expense saved successfully")
        
        return redirect('expenses')

@login_required(login_url='/auth/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'date': str(expense.date),
        'categories': categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']


        if not amount :
            messages.error(request, "Amount is required!")
            return render(request, 'expenses/add_expense.html', context=context)
        
        if not description :
            messages.error(request, "Description is required!")
            return render(request, 'expenses/add_expense.html', context=context)
        
        expense.owner = request.user
        expense.amount = amount
        expense. date = expense_date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, "Expense updated successfully")

        return redirect('expenses')

@login_required(login_url='/auth/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")

    return redirect('expenses')

@login_required(login_url='/auth/login')
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    
def expense_category_summary(request):
    todaysDate = datetime.date.today()
    sixMonthsAgo = todaysDate - datetime.timedelta(days = 30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=sixMonthsAgo, date__lte=todaysDate)

    finalrep = {

    }

    def get_category(expense):
        return expense.category
    
    categoryList = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filteredByCategory = expenses.filter(category=category)

        for i in filteredByCategory:
            amount += i.amount
        return amount

    for x in expenses:
        for y in categoryList:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def summary_expense(request):
    return render(request, 'expenses/summary_expense.html')