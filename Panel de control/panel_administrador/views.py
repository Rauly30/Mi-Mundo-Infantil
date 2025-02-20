from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def is_administrador(user):
    return user.is_superuser

@login_required
@user_passes_test(is_administrador)
def panel_administrador(request):
    return render(request, 'panel-administrador.html')