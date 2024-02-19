from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages

# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email in use.'}, status=409)
        
        return JsonResponse({'email_valid': True})
    
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'User name should only contain alphanumeric characters.'})
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'User name is alreay taken!'}, status=409)
        
        return JsonResponse({'username_valid': True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # Get uset data
        # Validate
        # Create user acount

        context = {
            'fieldValues': request.POST
        }

        username = request.POST['username'] 
        email = request.POST['email'] 
        password = request.POST['password'] 

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short!")
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username, email)
                user.set_password(password)
                user.save()
                messages.success(request, "Account successfully created.")
                return render(request, 'authentication/register.html')
                
                    
    
        return render(request, 'authentication/register.html')