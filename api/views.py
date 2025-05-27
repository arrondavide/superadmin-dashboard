import secrets
import string

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .models import PagePermission, Comment, CommentHistory
from .serializers import (
    UserSerializer, CreateUserSerializer, PagePermissionSerializer,
    CommentSerializer, CommentHistorySerializer
)
from .permissions import IsSuperAdmin

User = get_user_model()

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'set_permissions']:
            return [IsSuperAdmin()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Only super admin can create users
        if not request.user.is_super_admin:
            return Response({"detail": "Not allowed"}, status=403)
        password = generate_password()
        data = request.data.copy()
        data["password"] = password
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            # TODO: Send password via email
            return Response({"user": UserSerializer(user).data, "password": password})
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def set_permissions(self, request, pk=None):
        user = self.get_object()
        perms_data = request.data.get("permissions", [])
        for p in perms_data:
            obj, _ = PagePermission.objects.get_or_create(user=user, page=p["page"])
            obj.can_view = p.get("can_view", False)
            obj.can_edit = p.get("can_edit", False)
            obj.can_create = p.get("can_create", False)
            obj.can_delete = p.get("can_delete", False)
            obj.save()
        return Response({"success": True})

class PagePermissionViewSet(viewsets.ModelViewSet):
    queryset = PagePermission.objects.all()
    serializer_class = PagePermissionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return PagePermission.objects.all()
        return PagePermission.objects.filter(user=user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        page = self.request.query_params.get("page")
        queryset = Comment.objects.all()
        if page:
            queryset = queryset.filter(page=page)
        return queryset

    def perform_update(self, serializer):
        comment = self.get_object()
        CommentHistory.objects.create(
            comment=comment,
            modified_by=self.request.user,
            previous_text=comment.text,
        )
        serializer.save()

class CommentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommentHistory.objects.all()
    serializer_class = CommentHistorySerializer

    def get_queryset(self):
        if self.request.user.is_super_admin:
            return CommentHistory.objects.all()
        return CommentHistory.objects.none()