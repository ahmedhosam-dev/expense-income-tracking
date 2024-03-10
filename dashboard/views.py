from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/auth/login')
def index(request):
    context = {
        'userName': request.user,
    }

    if request.method == 'GET':
        return render(request, 'dashboard/index.html', context=context)
    
    if request.method == 'POST':
        return render(request, 'dashboard/index.html')