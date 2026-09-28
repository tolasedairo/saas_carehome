from accounts.services import get_user_care_homes


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.care_home = None

        if request.user.is_authenticated:
            care_homes = get_user_care_homes(request.user)

            if care_homes.count() == 1:
                request.care_home = care_homes.first()
            elif care_homes.exists():
                selected_care_home_id = request.session.get(
                    "care_home_id"
                )

                if selected_care_home_id:
                    request.care_home = care_homes.filter(
                        id=selected_care_home_id
                    ).first()

        return self.get_response(request)
