from rest_framework import serializers
from .models import GroupChat, Message, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='userprofile.avatar', read_only=True)
    bio = serializers.CharField(source='userprofile.bio', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'bio']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance

class GroupChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'members']
