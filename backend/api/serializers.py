from rest_framework import serializers
from .models import User, PagePermission, Comment, CommentHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_super_admin"]

class PagePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagePermission
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"

class CommentHistorySerializer(serializers.ModelSerializer):
    modified_by = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CommentHistory
        fields = "__all__"