from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import tokenGenerator


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

                email.send(False)

                messages.success(request, "Account successfully created. \n Please check your email to verify your account!")

                return render(request, 'authentication/register.html')
                
                    
    
        return render(request, 'authentication/register.html')
    

class VerificationView(View):
    def get(slef, request, uidb64, token):
        return redirect('login')