from fastapi import APIRouter, Depends

from secure_api.schemas.auth import UserResponse
from secure_api.models.user import User
from secure_api.services.user_repository import UserRepository
from secure_api.core.dependencies import (
    get_current_user,
    get_current_active_superuser,
    get_user_repository,
)

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="lista todos los usuarios, solo superusuarios",
)
async def list_users(
    _: User = Depends(get_current_active_superuser),
    repo: UserRepository = Depends(get_user_repository),
) -> list[UserResponse]:
    users = await repo.list_all()
    return [UserResponse(**u.to_dict()) for u in users]


@router.get(
    "/{username}",
    response_model=UserResponse,
    summary="Trae los datos de usuario por username, solo superusuarios",
)
async def get_user(
    username: str,
    _: User = Depends(get_current_active_superuser),
    repo: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    from fastapi import HTTPException, status
    user = await repo.find_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")
    return UserResponse(**user.to_dict())
