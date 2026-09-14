from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse


@login_required
def care_home_detail(request, slug):
    care_home = request.care_home

    if care_home is None or care_home.slug != slug:
        raise Http404

    return HttpResponse(
        f"Care home: {care_home.name}"
    )
