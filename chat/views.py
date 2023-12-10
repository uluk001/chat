from django.shortcuts import render
from .models import Chat, Message

def index(request):
    chats = Chat.objects.filter(buyer=request.user) | Chat.objects.filter(seller=request.user)
    context = {
        'chats': chats
    }
    return render(request, 'index.html', context)


def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    context = {
        'chat': chat,
        'messages': messages,
        'chat_id': chat_id,
    }
    return render(request, 'chat.html', context)