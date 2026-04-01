from users.models import User
from auth_core.jwt_service import decode_token


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_token(token)

            if payload:
                try:
                    user = User.objects.get(id=payload["user_id"], is_active=True)
                    request.user = user
                except User.DoesNotExist:
                    pass

        return self.get_response(request)