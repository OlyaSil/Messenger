from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupChatViewSet, MessageViewSet, UserProfileViewSet, UserViewSet, group_chat

router = DefaultRouter()
router.register(r'groupchats', GroupChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat/<str:group_identifier>/', group_chat, name='group_chat'),
]
