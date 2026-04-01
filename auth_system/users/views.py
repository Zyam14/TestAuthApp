from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .models import User
from auth_core.jwt_service import generate_token


@api_view(["POST"])
def register(request):

    data = request.data

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=400)

    if data["password"] != data["password_confirm"]:
        return Response({"error": "Passwords do not match"}, status=400)

    user = User(
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
    )
    user.set_password(data["password"])
    user.save()

    return Response({"message": "User created"})


@api_view(["POST"])
def login(request):
    data = request.data

    try:
        user = User.objects.get(email=data["email"], is_active=True)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.check_password(data["password"]):
        return Response({"error": "Invalid credentials"}, status=400)

    token = generate_token(user.id)

    return Response({"token": token})


@api_view(["POST"])
def logout(request):
    return Response({"message": "Logout successful"})

@api_view(["PUT"])
def update_profile(request):
    if not request.user:
        return Response(status=401)

    user = request.user
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)
    user.save()

    return Response({"message": "Updated"})


@csrf_exempt
@api_view(["DELETE"])
def delete_user(request):
    user = request.user

    if not user or not user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=401)

    user.is_active = False
    user.save()

    return Response({"message": "User deactivated"})