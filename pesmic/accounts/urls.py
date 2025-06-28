from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='register'),
     path("login/", views.LoginView.as_view(), name="user-login"),
    path("logout/", views.LogoutView.as_view(), name="user-logout"),
    path("refresh/", views.CookieTokenRefreshView.as_view(), name="token-refresh"),
    path("resetpassword/", views.RequestPasswordResetView.as_view(), name="password-reset"),
    path("confirmresetpassword/", views.ConfirmPasswordResetView.as_view(), name="confirm-password-reset"),
    path("changepassword/", views.ChangePasswordView.as_view(), name="change-password"),



    path('profile/', views.UserProfileCreateView.as_view(), name='accounts'),
    path("my-profile/", views.UserProfileUpdateView.as_view()),
    path("brand/", views.BrandProfileView.as_view()),
    path("brands/", views.BrandsView.as_view()),
    path("brands/<str:username>/", views.BrandView.as_view()),
    path("my-brand/", views.BrandGetUpdateView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)


