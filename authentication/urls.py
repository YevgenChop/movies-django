from django.urls import path
from .views import (
    GoogleLoginRedirectView, TokenObtainPairView, TokenRefreshView,
    GoogleLoginView, RegisterView, LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('redirect/google/', GoogleLoginRedirectView.as_view(),
         name='google_login_redirect'),
    path('callback/google/', GoogleLoginView.as_view(),
         name='google_login_callback'),
]
