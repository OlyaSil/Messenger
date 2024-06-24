# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'groupchats', GroupChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/<str:group_identifier>/', group_chat, name='group_chat'),
    path('api/messages/<str:group_identifier>/', get_messages, name='get_messages'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]
