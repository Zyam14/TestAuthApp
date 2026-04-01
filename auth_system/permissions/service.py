from .models import AccessRule, BusinessElement


from users.models import UserRole
def check_permission(user, element_name, action):
    if not user or not user.is_authenticated:
        return False

    roles = UserRole.objects.filter(user=user).values_list("role", flat=True)

    element = BusinessElement.objects.filter(name=element_name).first()
    if not element:
        return False

    rules = AccessRule.objects.filter(role_id__in=roles, element=element)

    for rule in rules:
        if getattr(rule, action, False):
            return True

    return False