from rest_framework import viewsets, permissions
from .models import GroupChat, Message, UserProfile
from .serializers import GroupChatSerializer, MessageSerializer, UserProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404


class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def home(request):
    groups = GroupChat.objects.all()
    return render(request, 'chat/home.html', {'groups': groups})

@login_required
def group_chat(request, group_identifier):
    try:
        # Сначала пытаемся интерпретировать идентификатор как целое число и искать по pk
        group_id = int(group_identifier)
        group = get_object_or_404(GroupChat, pk=group_id)
    except ValueError:
        # Если это не число, ищем по имени
        group = get_object_or_404(GroupChat, name=group_identifier)
    except GroupChat.DoesNotExist:
        # Если группа не найдена, возвращаем 404
        raise Http404("No GroupChat matches the given query.")

    return render(request, 'chat/group_chat.html', {'group': group})