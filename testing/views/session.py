from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import HttpResponse
from testing.views import NoAuthTokenView
from django.contrib.auth import get_user_model

User = get_user_model()

def AutoLoginAdmin(request):
    user = User.objects.filter(is_superuser=True).first()
    if user:
        login(request, user)
        return redirect('/admin/')
    return HttpResponse("Admin kullanıcı bulunamadı.")