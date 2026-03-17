from fastapi import APIRouter, Depends
from secure_api.models.user import User
from secure_api.core.dependencies import get_current_user, get_current_active_superuser

router = APIRouter(prefix="/resources", tags=["Protected Resources"])


@router.get("/dashboard", summary="Cualquier usuario autenticado")
async def dashboard(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "message": f"Bienvenido, {current_user.username}!",
        "user_id": current_user.id,
        "is_superuser": current_user.is_superuser,
    }


@router.get("/admin", summary="Superuser only")
async def admin_panel(
    current_user: User = Depends(get_current_active_superuser),
) -> dict:
    return {"message": "Admin panel", "superuser": current_user.username}
