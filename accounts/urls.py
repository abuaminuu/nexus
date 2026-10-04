from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserRegistrationView
from accounts import views

app_name = "accounts"

urlpatterns = [
    # 1. HTML BROWSER ROUTES (Session-based for  UI & Social)
    path("login/", views.login_view, name="login-view"),
    path("signup/", views.signup_view, name="signup-view"),
    path("logout/", views.logout_view, name="logout-view"),
    path("landing/", views.landing_page, name="landing-page"),
    
    # 2. REST API ROUTES (JWT-based for Headless Commerce & Postman)
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("api-token/", TokenObtainPairView.as_view(), name="api-token"),
    path("api-refresh/", TokenRefreshView.as_view(), name="token-refresh")
]
