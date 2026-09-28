from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from accounts.services import get_user_care_homes


@login_required
def care_home_detail(request, slug):
    care_home = request.care_home

    if care_home is None or care_home.slug != slug:
        raise Http404

    return HttpResponse(
        f"Care home: {care_home.name}"
    )


@login_required
def select_care_home(request, pk):
    if request.method != "POST":
        raise Http404

    care_home = get_user_care_homes(request.user).filter(
        pk=pk,
    ).first()

    if care_home is None:
        raise Http404

    request.session["care_home_id"] = care_home.id
    request.session.save()

    return redirect(
        "care_home_detail",
        slug=care_home.slug,
    )


@login_required
def care_home_select(request):
    care_homes = get_user_care_homes(request.user)

    return render(
        request,
        "tenancy/care_home_select.html",
        {
            "care_homes": care_homes,
        },
    )