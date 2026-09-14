from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import CareHomeMembership
from tenancy.models import CareHome


class CareHomeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcarer",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            username="othercarer",
            password="test-password",
        )

        self.sunrise = CareHome.objects.create(
            name="Sunrise Care Home",
            slug="sunrise-care-home",
        )

        self.sunset = CareHome.objects.create(
            name="Sunset Care Home",
            slug="sunset-care-home",
        )

        CareHomeMembership.objects.create(
            user=self.user,
            care_home=self.sunrise,
            role="carer",
        )

        CareHomeMembership.objects.create(
            user=self.other_user,
            care_home=self.sunset,
            role="carer",
        )

    def test_member_can_access_care_home(self):
        self.client.login(
            username="testcarer",
            password="test-password",
        )

        response = self.client.get(
            reverse(
                "care_home_detail",
                kwargs={"slug": "sunrise-care-home"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunrise Care Home")

    def test_member_cannot_access_another_care_home(self):
        self.client.login(
            username="testcarer",
            password="test-password",
        )

        response = self.client.get(
            reverse(
                "care_home_detail",
                kwargs={"slug": "sunset-care-home"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(
            reverse(
                "care_home_detail",
                kwargs={"slug": "sunrise-care-home"},
            )
        )

        self.assertEqual(response.status_code, 302)
