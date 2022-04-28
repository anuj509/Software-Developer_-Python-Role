from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from . import views

urlpatterns = [
    path('',views.UserAPIView.as_view(),name="user"),
    path('auth/token',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('auth/token/refresh',TokenRefreshView.as_view(),name="token_refresh"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
