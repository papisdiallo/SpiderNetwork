from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import allowedToChatWith
from Connection.models import ConnectionsList
from django.db.models import Q
from .models import singleOneToOneRoom
User = get_user_model()

# need to pass also the test_func user to see if they are friends or not.


@login_required
@allowedToChatWith
def Chat(request, username, *args, **kwargs):
    current_user = request.user
    current_user_connections = ConnectionsList.objects.get(
        user=current_user).connections.all()
    other_user = User.objects.get(username=username)
    lookup = Q(first_user=current_user, second_user=other_user) | Q(
        first_user=other_user, second_user=current_user)
    room = singleOneToOneRoom.objects.filter(lookup)
    msges = room.first().messages.all()
    context = {"other_user": other_user,
               "all_users": current_user_connections, "msges": msges, }
    return render(request, "landing/message.html", context)
