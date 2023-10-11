from fastapi import APIRouter, HTTPException, status, Request
from database.basemodels import UserSchema
from misc.hasher import Hasher
from starlette.responses import RedirectResponse, HTMLResponse
from database.functions import create_new_user, get_user_by_username
from fastapi.templating import Jinja2Templates
from misc.token import create_jwt_token

from pydantic import BaseModel

templates = Jinja2Templates(directory="../templates/auth_templates")


router = APIRouter()


class LoginData(BaseModel):
    login: str
    password: str


async def get_user(username: str) -> UserSchema or None:
    user_data = await get_user_by_username(username)
    if not user_data:
        return None
    return UserSchema(login=user_data.login, hashed_password=user_data.hashed_password)


async def validate_password(password: str, user: UserSchema) -> bool:
    return Hasher.hash_password(password) == user.hashed_password


async def add_user_to_database(user: UserSchema):
    if await get_user(user.login):
        return None

    await create_new_user(user)
    return True


@router.get("/auth/login", response_class=HTMLResponse)
async def auth_main_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/auth/login")
async def login(login_data: LoginData):
    user = await get_user(username=login_data.login)
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин/пароль")
    password_valid = await validate_password(login_data.password, user)
    if not password_valid:
        raise HTTPException(status_code=400, detail="Неверный логин/пароль")

    encoded_jwt = create_jwt_token(user)

    response = RedirectResponse(
        url=f"/main_page",
        status_code=status.HTTP_303_SEE_OTHER,
        headers={'Token': encoded_jwt}
    )
    response.set_cookie(
        key="Token",
        value=encoded_jwt,
        max_age=1800,
        secure=True,
        httponly=True,
    )
    return response


@router.get("/auth/register")
async def auth_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/auth/register")
async def register(login_data: LoginData):
    try:
        user = UserSchema(login=login_data.login, hashed_password=Hasher.hash_password(login_data.password))
    except:
        raise HTTPException(status_code=400, detail="Введены недопустимые данные!")

    if not await add_user_to_database(user):
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже зарегистрирован")

    return RedirectResponse(
        url='/auth/login',
        status_code=status.HTTP_303_SEE_OTHER
    )
