from django.test import TestCase, client as test_client
from django.contrib.auth.models import User

from library_app.models import Client

class TestAddFunds(TestCase):
    _url = '/profile/'

    def setUp(self) -> None:
        self.test_client = test_client.Client()
        self.user = User.objects.create(username='user', password='user')
        self.library_client = Client.objects.create(user=self.user, money=0)
        self.test_client.force_login(self.user)

    def test_negative_funds(self):
        self.test_client.post(self._url, {'money': -1})
        self.assertEqual(self.library_client.money, 0)

    def test_add_funds(self):
        self.test_client.post(self._url, {'money': 1})
        self.library_client.refresh_from_db()

        self.assertEqual(self.library_client.money, 1)
