import pytest
from django.urls import reverse
from rest_framework.test import APIClient,force_authenticate,APIRequestFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import User
from blog.api.v1.views import PostModelViewSet

@pytest.mark.django_db
class TestPost:

    def test_post_response_200(self):
        client = APIClient()
        user = get_user_model().objects.create_user(email="test@email.com",password="test")
        client.force_authenticate(user)
        response = client.get(reverse("blog:api-v1:post-list"))
        assert response.status_code == 200


# class TestPost2(TestCase):

#     def test_post(self):
#         user = User.objects.create_user(email="test@email.com",password="test")
#         factory = APIRequestFactory()
#         request = factory.get(reverse("blog:api-v1:post-list"))
#         force_authenticate(request,user)
#         response = PostModelViewSet.as_view({"get":"list"})(request)
#         self.assertEqual(response.status_code,200)


