from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import timedelta
from src.api.handlers.users.user import user_router, _create_new_user, _delete_user, _get_user_by_id, _update_user
from src.api.handlers.auth.auth import login_router, authenticate_user
from src.api.models import UserCreate, DeletedUserResponse, ShowUser, UpdatedUserResponse, UpdatedUserRequest, Token
from src.db.session import get_db 
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES



# User 
@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser: 
    return await _create_new_user(body, db)

@user_router.delete("/", response_model=DeletedUserResponse)
async def delete_user(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
    ) -> DeletedUserResponse: 
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None: 
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return DeletedUserResponse(delete_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
    ) -> ShowUser: 
    user_info = await _get_user_by_id(user_id, db)
    if user_info is None: 
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user_info

@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user(user_id: UUID, body: UpdatedUserRequest, db: AsyncSession = Depends(get_db)) -> UpdatedUserResponse: 
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    updated_user_id = await _update_user(updated_user_params=updated_user_params, db=db, user_id=user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)

# Login
@login_router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2AuthorizationCodeBearer = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        
    )