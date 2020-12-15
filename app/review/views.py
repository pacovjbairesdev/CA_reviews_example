from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Review

from review import serializers


class ReviewViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin
                    ):
    """Base ViewSet for creating and listing Review Objects in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        """Return reviews for the current authenticated user only"""
        return self.queryset.filter(
                reviewer=self.request.user
                ).order_by('-title')

    def perform_create(self, serializer):
        """Create a new Review"""
        serializer.save(
                reviewer=self.request.user,
                ip=self.request.META['REMOTE_ADDR']
                )
