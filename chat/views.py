from django.shortcuts import render
from django.contrib.auth.models import User

from core.models import ChatMessage


def chat(request, userId):
    user = User.objects.get(id=userId)
    requestUser = request.user
    messages = ChatMessage.objects.filter(from_user__in=[requestUser.id, userId], to_user__in=[requestUser.id, userId])
    print(messages)
    context = {
        'user': user,
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)