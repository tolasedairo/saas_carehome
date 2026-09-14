from django.contrib.auth.models import User
from django.db import models

from tenancy.models import CareHome


class CareHomeMembership(models.Model):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("senior_carer", "Senior Carer"),
        ("carer", "Carer"),
        ("administrator", "Administrator"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="care_home_memberships",
    )
    care_home = models.ForeignKey(
        CareHome,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "care_home"],
                name="unique_user_care_home_membership",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.care_home.name}"
