from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import CareHomeMembership
from accounts.services import get_user_care_homes
from tenancy.models import CareHome


class GetUserCareHomesTests(TestCase):
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

        self.inactive = CareHome.objects.create(
            name="Inactive Care Home",
            slug="inactive-care-home",
            is_active=False,
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

        CareHomeMembership.objects.create(
            user=self.user,
            care_home=self.inactive,
            role="carer",
        )

    def test_returns_only_users_active_care_homes(self):
        care_homes = get_user_care_homes(self.user)

        self.assertEqual(list(care_homes), [self.sunrise])

    def test_does_not_return_another_users_care_home(self):
        care_homes = get_user_care_homes(self.user)

        self.assertNotIn(self.sunset, care_homes)

    def test_does_not_return_inactive_care_home(self):
        care_homes = get_user_care_homes(self.user)

        self.assertNotIn(self.inactive, care_homes)
