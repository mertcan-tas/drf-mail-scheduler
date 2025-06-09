from django.urls import path
from testing.views import NoAuthTokenView, AutoLoginAdmin, SendTestEmail
from decouple import config

urlpatterns = [
    path('testing/auth/session/', AutoLoginAdmin, name='testing-auth-session'),
    path('testing/auth/api/', NoAuthTokenView.as_view(), name='testing-auth-api'),
    path('testing/send-test-email/', SendTestEmail, name='send_test_email'),
]