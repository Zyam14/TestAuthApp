from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from permissions.decorators import permission_required


@api_view(["GET"])
@permission_required("products", "read")
def get_products(request):
    return Response([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Phone"},
        {"id": 3, "name": "PC"},
    ])