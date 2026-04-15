from fastapi import APIRouter, Depends

from secure_api.core.openapi import responses_superuser
from secure_api.schemas.auth import UserResponse
from secure_api.models.user import User
from secure_api.services.user_repository import UserRepository
from secure_api.core.dependencies import (
    get_current_active_superuser,
    get_user_repository,
)

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Devuelve todos los usuarios registrados. **Solo superusuarios.**",
    responses={
        **responses_superuser(),
        200: {"description": "Lista de perfiles de usuario."},
    },
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
    summary="Obtener usuario por nombre",
    description="Busca por `username`. **Solo superusuarios.**",
    responses={
        **responses_superuser(),
        200: {"description": "Usuario encontrado."},
        404: {"description": "No existe un usuario con ese `username`."},
    },
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
