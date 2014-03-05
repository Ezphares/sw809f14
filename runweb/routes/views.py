# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def planner(request):
    return render(request, 'routing.html', {})

