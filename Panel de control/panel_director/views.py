from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def is_director(user):
    return user.groups.filter(name='Directores').exists()

@login_required
@user_passes_test(is_director)
def panel_director(request):
    return render(request, 'panel-director.html')