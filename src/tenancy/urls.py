from django.urls import path

from tenancy import views

urlpatterns = [
    path(
        "care-homes/<slug:slug>/",
        views.care_home_detail,
        name="care_home_detail",
    ),
    path(
        "care-homes/select/<int:pk>/",
        views.select_care_home,
        name="select_care_home",
    ),
    path(
    "care-homes/select/",
    views.care_home_select,
    name="care_home_select",
    ),
]
