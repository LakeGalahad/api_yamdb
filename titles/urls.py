from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import RegisterView, TokenView, UserViewSet
from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/email/', RegisterView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls))
]
