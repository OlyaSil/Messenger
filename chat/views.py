# views.py
from rest_framework import viewsets, permissions
from .models import GroupChat, Message, UserProfile
from .serializers import GroupChatSerializer, MessageSerializer, UserProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import *

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
        group = get_object_or_404(GroupChat, pk=group_identifier)
    except ValueError:
        group = get_object_or_404(GroupChat, name=group_identifier)
    except GroupChat.DoesNotExist:
        raise Http404("No GroupChat matches the given query.")

    return render(request, 'chat/group_chat.html', {'group': group})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, group_identifier):
    try:
        group = GroupChat.objects.get(name=group_identifier)
        messages = Message.objects.filter(group=group).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except GroupChat.DoesNotExist:
        return Response({'error': 'Group does not exist'}, status=404)

@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'chat/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@api_view(['GET'])
def get_group_members(request, group_identifier):
    try:
        group = GroupChat.objects.get(name=group_identifier)
        members = group.members.all()
        members_data = []
        for member in members:
            profile = UserProfile.objects.get(user=member)
            members_data.append({
                'username': member.username,
                'email': member.email,
                'avatar': profile.avatar.url if profile.avatar else '',
                'bio': profile.bio,
            })
        return Response(members_data)
    except GroupChat.DoesNotExist:
        return Response({'error': 'Group does not exist'}, status=404)