from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .security import get_current_user, get_db
from .models.rbac import Role, Permission, UserRole, RolePermission


def user_permissions(db: Session, user_id: int) -> set[str]:
    # join roles -> role_permissions -> permissions
    perms: set[str] = set()
    q = (
        db.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(Role, Role.id == RolePermission.role_id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
    )
    for (code,) in q.all():
        perms.add(code)
    return perms


def require_permission(code: str):
    def _dep(user=Depends(get_current_user), db: Session = Depends(get_db)):
        perms = user_permissions(db, user.id)
        if code not in perms and "admin" not in perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {code}",
            )
        return True

    return _dep
