from django.contrib.auth.models import User
from tenancy.models import CareHome


def get_user_care_homes(user: User):
    """
    Return the active care homes this user belongs to.
    """
    return CareHome.objects.filter(
        memberships__user=user,
        is_active=True,
    ).distinct()
