from app.models.user import UserRole


def can_acknowledge(role):

    return role in {
        UserRole.engineer,
        UserRole.commander,
        UserRole.admin,
    }


def can_resolve(role):

    return role in {
        UserRole.commander,
        UserRole.admin,
    }