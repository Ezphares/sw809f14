# Create your views here.
from django.shortcuts import render


def planner(request):
    return render(request, 'routing.html', {})

