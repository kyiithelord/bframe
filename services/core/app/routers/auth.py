from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..security import get_db, get_password_hash, verify_password, create_access_token
from ..schemas.auth import Token
from ..models.user import User
from ..models.tenant import Tenant
from ..config import settings
from ..models.rbac import Role, Permission, UserRole, RolePermission

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return Token(access_token=token)

@router.post("/bootstrap")
def bootstrap(db: Session = Depends(get_db)):
    # Create default tenant and superuser if not existing
    # Use safe defaults if env vars are missing to avoid 500s
    super_email = settings.SUPERUSER_EMAIL or "admin@bframe.local"
    super_password = settings.SUPERUSER_PASSWORD or "admin123"

    created = {"tenant": False, "admin": False}

    tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
    if not tenant:
        tenant = Tenant(name="Default", slug="default")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        created["tenant"] = True

    admin = db.query(User).filter(User.email == super_email).first()
    if not admin:
        admin = User(
            email=super_email,
            hashed_password=get_password_hash(super_password),
            tenant_id=tenant.id,
        )
        db.add(admin)
        db.commit()
        created["admin"] = True

    # Seed RBAC: admin role and basic permissions
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Superuser role")
        db.add(admin_role)
        db.commit()

    # Ensure admin permission and some module perms exist
    def ensure_perm(code: str, desc: str = ""):
        p = db.query(Permission).filter(Permission.code == code).first()
        if not p:
            p = Permission(code=code, description=desc)
            db.add(p)
            db.commit()
        # grant to admin_role
        rp = db.query(RolePermission).filter(RolePermission.role_id == admin_role.id, RolePermission.permission_id == p.id).first()
        if not rp:
            rp = RolePermission(role_id=admin_role.id, permission_id=p.id)
            db.add(rp)
            db.commit()

    for code in [
        "admin",
        "crm.read",
        "crm.write",
        "tenants.read",
        "modules.read",
    ]:
        ensure_perm(code)

    # assign admin role to admin user
    ur = db.query(UserRole).filter(UserRole.user_id == admin.id, UserRole.role_id == admin_role.id).first()
    if not ur:
        ur = UserRole(user_id=admin.id, role_id=admin_role.id)
        db.add(ur)
        db.commit()

    return {"status": "ok", "created": created, "email": super_email, "role": "admin"}
