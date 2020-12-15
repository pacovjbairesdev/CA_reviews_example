from rest_framework import serializers

from core import models


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes a Review Object"""

    class Meta:
        model = models.Review
        fields = (
                 'id', 'title', 'rating',
                 'summary', 'submission_date', 'company'
                 )
        read_only_fields = ('id', 'submission_date')
