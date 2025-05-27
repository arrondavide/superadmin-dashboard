from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PagePermissionViewSet, CommentViewSet, CommentHistoryViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'permissions', PagePermissionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'comment-history', CommentHistoryViewSet)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]