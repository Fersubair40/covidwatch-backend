from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from core.models import InteractionRecord


class APITests(TestCase):
    def test_api_requires_an_app_authentication_header(self):
        stored_value = "gobbledegook"
        resp = self.client.post(reverse("store_interaction_record"), {'stored_value': stored_value})
        self.assertEqual(400, resp.status_code)
        self.assertEqual(0, InteractionRecord.objects.all().count())

        resp = self.client.post(
            reverse("store_interaction_record"),
            {'stored_value': stored_value},
            **{'HTTP_X_APP_SECRET_KEY': settings.APP_SECRET_KEY}
        )
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, InteractionRecord.objects.filter(stored_value=stored_value).count())
