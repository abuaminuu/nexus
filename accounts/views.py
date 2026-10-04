from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth.decorators import login_required
User = get_user_model()

# Create your views here.
# 1. REST API VIEWS (For Swagger / Headless)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

# 2. HTML TEMPLATE VIEWS (For Browser UI)

@login_required
def landing_page(request):
    """
    Renders the central Launchpad/Gateway after login, 
    allowing users to choose between Commerce API and Social Network.
    """
    return render(request, "accounts/landing.html")


def login_view(request):
    # trying to login
    if request.method == "GET" and request.user.is_authenticated == False:
        return render(request, "accounts/auth.html")
    
    if request.method == "GET" and request.user.is_authenticated:
        return redirect("accounts:landing-page")
        
    if request.method == "POST" and request.user.is_authenticated == False:
        email = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the choice landing page instead of hardcoded url
            return redirect("accounts:landing-page")

        # esle invalid credentials 
        return render(request, "accounts/auth.html", {"error": "Invalid email or password."})

    # else invalid method
    return render(request, "accounts/auth.html", {"error": "Invalid method."})
    


def signup_view(request):
    """Processes signup form submissions from auth.html."""
    if request.method == "POST" and request.user.is_authenticated == False:
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            # Auto-login after registration
            login(request, user)  
            return redirect("accounts:landing-page")
        # esle invalid serializer
        return render(request, "accounts/auth.html", {"errors": serializer.errors})

    # else not POST !
    return redirect("accounts:login-view")

def logout_view(request):
    """Logs the user out and redirects to auth page."""
    logout(request)
    return redirect("accounts:login-view")
