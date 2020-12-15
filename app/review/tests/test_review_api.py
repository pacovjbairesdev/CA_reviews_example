from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Review
from recipe.serializers import ReviewSerializer


REVIEW_URL = reverse('review')

def create_dummy_review(user, title='Review 1'):
    """Simple function for creating reviews of a user"""
    review = Review.objects.create(
                user=user,
                rating=rating,
                title=title,
                summary='This is my first review!!!',
                ip='190.190.190.1',
                company='Test Company',
                )
    return review


class PublicReviewApiTests(TestCase):
    """Test that authentication is required for the review API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Check that login is required to access the endpoint"""
        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewApiTests(TestCase):
    """Test the authorized user review API"""

    def setUp(self):
        self.client = APIClient()
        self.user = ().objects.create_user(
            'test@test.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_review_list(self):
        """Test retrieving a list of reviews"""

        review1 = create_dummy_review(self.user)
        review2 = create_dummy_review(self.user,'Review 2')

        res = self.client.get(REVIEW_URL)

        Reviews = Review.objects.all().order_by('-title')
        serializer = ReviewSerializer(Reviews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_review_limited_to_user(self):
        """Check that Reviews for the authenticated user are returned"""
        user2 = ().objects.create_user(
            'test2@test.com',
            'password2'
        )
        review1 = create_dummy_review(self.user)
        create_dummy_review(user2, 'Review X1')
        create_dummy_review(user2, 'Review X2')

        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], review1.title)

    def test_create_review_successful(self):
        """Check that Reviews are created"""
        review1 = create_dummy_review(self.user)

        exists = Review.objects.filter(
            user=self.user,
            title=review1.title,
        ).exists()

        self.assertTrue(exists)

    def test_create_review_invalid(self):
        """Test creating invalid Review fails"""
        payload = {'title': ''}
        res = self.client.post(REVIEW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
