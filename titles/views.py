from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review, Comment, Title
from .permissions import IsAuthorOrStaffOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly &
        IsAuthorOrStaffOrReadOnly
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = get_list_or_404(Review, title__id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly &
        IsAuthorOrStaffOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
