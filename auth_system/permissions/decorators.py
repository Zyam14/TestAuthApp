from rest_framework.response import Response
from .service import check_permission

def permission_required(element, action):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if not request.user or not request.user.is_authenticated:
                return Response({"error": "Unauthorized"}, status=401)

            if not check_permission(request.user, element, action):
                return Response({"error": "Forbidden"}, status=403)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator