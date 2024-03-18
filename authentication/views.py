from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import tokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from userpreferences.models import UserPreferences
from income.models import Source
from expenses.models import Category

# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

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
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = tokenGenerator.make_token(user)
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs = {
                    'uidb64': uidb64,
                    'token': token,
                })
                actiavteURL = f"http://{domain}{link}"

                email = EmailMessage(
                    "Active EXIN account", # Email subject
                    f"Hi {user.username},\n\nClick this link to verify your account\n{actiavteURL}", # Eamil body
                    "noreply@exin.com", # From
                    [email], # To
                )

                EmailThread(email).start()

                messages.success(request, "Account successfully created. \n Please check your email to verify your account!")

                return render(request, 'authentication/register.html')
                
                    
    
        return render(request, 'authentication/register.html')
    

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not tokenGenerator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                messages.error(request, 'Account not activate, check your email')
                return redirect('login')
            
            user.is_active = True
            user.save()


            print("Hello, world!")
            
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        userName = request.POST['username'] 
        password = request.POST['password']


        if userName and password:
            user = auth.authenticate(username=userName, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username} you are now logged in.")
        
                    if not UserPreferences.objects.filter(user=request.user).exists():
                        userPreferences = UserPreferences.objects.create(user=request.user, currency="USD -- United States Dollar")
                        userPreferences.save()
                        Category.objects.create(user=request.user, name="Food")
                        Source.objects.create(user=request.user, name="Work")
                        
                    return redirect('dashboard')

                messages.error(request, "Account is not activate, please check your email!")
                return render(request, 'authentication/login.html')

            messages.error(request, "Invalid credentials, try again!")
            return render(request, 'authentication/login.html')
        
        messages.error(request, "Please fill all fields!")
        return render(request, 'authentication/login.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        
        return redirect('login')

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/reset-password.html', context=context)
        
        user = User.objects.filter(email=email)

        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            domain = get_current_site(request).domain
            link = reverse('reset-user-password', kwargs = {
                'uidb64': uidb64,
                'token': token,
            })
            resetURL = f"http://{domain}{link}"

            email = EmailMessage(
                "Password reset instructions", # Email subject
                f"Hi {user[0].username},\n\nClick this link to reset your password\n{resetURL}", # Email body
                "noreply@exin.com", # From
                [email], # To
            )

            EmailThread(email).start()

            messages.success(request, "Please check your email to reset your password!")

            return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        return render(request, 'authentication/set-new-password.html', context=context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Password not match!')
            return render(request, 'authentication/set-new-password.html', context=context)
        
        if len(password) < 6:
            messages.error(request, 'Password too short! must be bigger than 6.')
            return render(request, 'authentication/set-new-password.html', context=context)
        
        try:

            userId = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=userId)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfull, login with new password.')
            return redirect('login')
        
        except Exception as ex:
            messages.warning(request, 'Something went wrong, try again!')
            return render(request, 'authentication/set-new-password.html', context=context)
