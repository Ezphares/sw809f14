# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def session_login(request):
    redirect = '/routes/planner/' #TODO overview
    
    #Check if an alternate redirect was requested
    if 'next' in request.REQUEST:
        redirect = request.REQUEST['next']

    # Do not log already authenticated users in
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    # Get requests get the form
    if request.method == 'GET':
        return render(request, 'login.html', {'redirect': redirect})

    # Post requests attempt to authenticate
    else:
        user = authenticate(username = request.REQUEST['username'], password = request.REQUEST['password'])
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password', 'redirect': redirect})

def session_logout(request):
	# Clears the session and returns home
    logout(request)
    return HttpResponseRedirect('/')
