from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Group, Message
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def HomeView(request):
    groups = Group.objects.all()
    user = request.user
    context = {
        'groups': groups,
        'user': user
    }
    return render(request, template_name='chat/home.html', context=context)



def GroupChatView(request, uuid):
    group = get_object_or_404(Group, uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden('You are not a member of this group, use join button')
    
    messages = group.message_set.all()
    events = group.event_set.all()
    group_members = group.members.all()

    message_and_event_list = [*messages, *events]
    sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)
    
    context = {
        'message_and_event_list': sorted_message_event_list,
        'group_members': group_members
    }

    return render(request, template_name='chat/groupchat.html', context=context)

