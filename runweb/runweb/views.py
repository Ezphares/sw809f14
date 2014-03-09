# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt #TODO: Apps should get a csrf key as well so we can track them, later
def session_login(request, as_json = False):
    redirect = '/routes/'
    
    #Check if an alternate redirect was requested
    if 'next' in request.REQUEST:
        redirect = request.REQUEST['next']

    # Do not log already authenticated users in
    if request.user.is_authenticated():
        if not as_json:
            return HttpResponseRedirect(redirect)
        else:
            return HttpResponse('{"status": "OK"}')

    # Get requests get the form
    if request.method == 'GET':
        if not as_json:
            return render(request, 'login.html', {'redirect': redirect})
        else:
            return HttpResponse('{"status": "ERROR"}')

    # Post requests attempt to authenticate
    else:
        if (not 'username' in request.REQUEST) or (not 'password' in request.REQUEST):
            if not as_json:
                return render(request, 'login.html', {'error': 'You must enter a username and password', 'redirect': redirect})
            else:
                return HttpResponse('{"status": "ERROR"}')
			
        user = authenticate(username = request.REQUEST['username'], password = request.REQUEST['password'])
        if user:
            login(request, user)
            if not as_json:
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponse('{"status": "OK"}')
        else:
            if not as_json:
                return render(request, 'login.html', {'error': 'Invalid username or password', 'redirect': redirect})
            else:
                return HttpResponse('{"status": "ERROR"}')

def session_logout(request):
	# Clears the session and returns home
    logout(request)
    return HttpResponseRedirect('/')
	
def register(request):
    # TODO: Use a django form for this view for easier validation, autofill etc, etc, later
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'register.html', {})

    else:
        if (not 'username' in request.REQUEST) or (not 'password' in request.REQUEST) or (not 'password_confirm' in request.REQUEST):
            return render(request, 'register.html', {'error': 'You must fill out the registration form'})

        if request.REQUEST['password'] != request.REQUEST['password_confirm']:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            user = User.objects.create_user(request.REQUEST['username'], '', request.REQUEST['password'])
            user.save()
            user = authenticate(username = request.REQUEST['username'], password = request.REQUEST['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        except:
            return render(request, 'register.html', {'error': 'Username already exists'})