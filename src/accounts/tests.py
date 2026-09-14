from django.contrib.auth.models import User
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.test import TestCase

from accounts.middleware.tenant import TenantMiddleware
from accounts.models import CareHomeMembership
from accounts.services import get_user_care_homes
from tenancy.models import CareHome


class TenantMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username="tenantuser",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="test-password",
        )

        self.care_home = CareHome.objects.create(
            name="Test Care Home",
            slug="test-care-home",
        )

        self.second_care_home = CareHome.objects.create(
            name="Second Care Home",
            slug="second-care-home",
        )

        self.other_care_home = CareHome.objects.create(
            name="Other Care Home",
            slug="other-care-home",
        )

        CareHomeMembership.objects.create(
            user=self.user,
            care_home=self.care_home,
            role="carer",
        )

        CareHomeMembership.objects.create(
            user=self.user,
            care_home=self.second_care_home,
            role="carer",
        )

        CareHomeMembership.objects.create(
            user=self.other_user,
            care_home=self.other_care_home,
            role="carer",
        )

    def get_authenticated_request(self):
        request = self.factory.get("/")

        SessionMiddleware(lambda request: None).process_request(request)
        request.session.save()

        AuthenticationMiddleware(lambda request: None).process_request(request)

        request.user = self.user

        return request

    def test_authenticated_user_gets_selected_care_home(self):
        request = self.get_authenticated_request()
        request.session["care_home_id"] = self.second_care_home.id
        request.session.save()

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertEqual(request.care_home, self.second_care_home)

    def test_user_with_multiple_care_homes_gets_no_care_home_without_selection(self):
        request = self.get_authenticated_request()

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertIsNone(request.care_home)

    def test_user_cannot_select_another_users_care_home(self):
        request = self.get_authenticated_request()
        request.session["care_home_id"] = self.other_care_home.id
        request.session.save()

        middleware = TenantMiddleware(lambda request: None)
        middleware(request)

        self.assertIsNone(request.care_home)

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
