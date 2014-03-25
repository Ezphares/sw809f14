# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from social.models import Friend

@login_required
def friendlist(request):
    friends_inbound = Friend.objects.filter(accepted = True, to_user = request.user)
    friends_outbound = Friend.objects.filter(accepted = True, from_user = request.user)
	
    friends = [x.from_user for x in friends_inbound]
    friends.extend([y.to_user for y in friends_outbound])
	
    return render(request, 'friends.html', {'friends': friends,
											'invites': Friend.objects.filter(to_user = request.user, accepted = False)})

@login_required
def remove_friend(request, id):
    try:
        friend = User.objects.get(pk = id)
        Friend.objects.filter(from_user = request.user, to_user = friend).delete()
        Friend.objects.filter(to_user = request.user, from_user = friend).delete()
    except:
        pass

    return HttpResponseRedirect('/social/friends/')

@login_required
@require_POST
def request_friend(request):
    # TODO: Handle prettier than throw
    try:
        other = User.objects.get(username = request.REQUEST['name'])
        if other == request.user:
            raise "Cannot befriend yourself"
        if (len(Friend.objects.filter(from_user = request.user, to_user = other)) > 0) or (len(Friend.objects.filter(to_user = request.user, from_user = other)) > 0):
            raise "Relation already exists"
        Friend(from_user = request.user, to_user = other).save()
    except:
        pass
		
    return HttpResponseRedirect('/social/friends/')

@login_required
def accept_request(request, id):
    try:
        f = Friend.objects.get(pk = id, to_user = request.user)
        f.accepted = True
        f.save()
    except:
        pass
    return HttpResponseRedirect('/social/friends/')
	
@login_required
def deny_request(request, id):
    try:
        f = Friend.objects.get(pk = id, to_user = request.user)
        f.delete()
    except:
        pass
    return HttpResponseRedirect('/social/friends/')