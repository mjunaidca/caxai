from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm

from ..data.db_config import get_db


from ..models.user_auth import RegisterUser, UserOutput, LoginResonse

from ..service.user_auth import service_signup_users, service_login_for_access_token


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResonse, tags=["Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    
    return await service_login_for_access_token(form_data, db)


@router.post("/users/signup/", response_model=UserOutput)
async def signup_users(
    user_data: RegisterUser, db: Session = Depends(get_db)
):
    return await service_signup_users(user_data, db)


# Sample Code for Authentication Route
# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
