from django.urls import path

from tenancy import views

urlpatterns = [
    path(
        "care-homes/<slug:slug>/",
        views.care_home_detail,
        name="care_home_detail",
    ),
]
