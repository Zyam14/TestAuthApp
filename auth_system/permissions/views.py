from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AccessRule, Role, BusinessElement
from .decorators import permission_required


@api_view(["POST"])
@permission_required("access_rules", "create")
def create_rule(request):
    data = request.data

    try:
        role = Role.objects.get(id=data["role_id"])
        element = BusinessElement.objects.get(id=data["element_id"])
    except (Role.DoesNotExist, BusinessElement.DoesNotExist):
        return Response({"error": "Invalid role or element"}, status=400)

    rule = AccessRule.objects.create(
        role=role,
        element=element,
        read=data.get("read", False),
        read_all=data.get("read_all", False),
        create=data.get("create", False),
        update=data.get("update", False),
        update_all=data.get("update_all", False),
        delete=data.get("delete", False),
        delete_all=data.get("delete_all", False),
    )

    return Response({"message": "Rule created", "id": rule.id})