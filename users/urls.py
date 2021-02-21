from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import RegisterView, TokenView, UserViewSet
router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/email/', RegisterView.as_view()),
    path('auth/token/', TokenView.as_view()),
    path('api/v1/', include(router.urls))
]
