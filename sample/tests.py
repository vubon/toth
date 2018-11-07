from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from sample.time_based_hash import get_toth

client = Client(HTTP_TOTH=get_toth('ServiceOne'), HTTP_SERVICE_NAME="ServiceOne")


class LoginTest(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "nothing1234"
        password = make_password(self.password, salt=None, hasher='default')
        User.objects.create(username=self.username, password=password)

    def test_login(self):
        data = {"username": self.username, "password": self.password}
        response = client.post(reverse("login-test"), data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)