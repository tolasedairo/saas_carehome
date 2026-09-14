from django.contrib.auth.models import User
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.test import TestCase

from accounts.middleware.tenant import TenantMiddleware
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



class TenantMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username="tenantuser",
            password="test-password",
        )

        self.care_home = CareHome.objects.create(
            name="Test Care Home",
            slug="test-care-home",
        )

        CareHomeMembership.objects.create(
            user=self.user,
            care_home=self.care_home,
            role="carer",
        )

    def get_authenticated_request(self):
        request = self.factory.get("/")

        SessionMiddleware(lambda request: None).process_request(request)
        request.session.save()

        AuthenticationMiddleware(lambda request: None).process_request(request)

        request.user = self.user

        return request

    def test_authenticated_user_gets_care_home(self):
        request = self.get_authenticated_request()

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertEqual(request.care_home, self.care_home)

    def test_user_without_membership_gets_no_care_home(self):
        user = User.objects.create_user(
            username="nomembership",
            password="test-password",
        )

        request = self.factory.get("/")
        request.user = user

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertIsNone(request.care_home)

    def test_anonymous_user_gets_no_care_home(self):
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertIsNone(request.care_home)
