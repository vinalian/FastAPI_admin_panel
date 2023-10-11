from fastapi import APIRouter, HTTPException, status, Request
from database.basemodels import UserSchema, ItemSchema
from starlette.responses import RedirectResponse
from database.functions import *
from database.basemodels import UpdateAndDeleteItemSchema, AppendSchema
from typing import List
from fastapi.templating import Jinja2Templates
from misc.token import validate_token

router = APIRouter()

templates = Jinja2Templates(directory="../templates/main_page_templates")


@router.get('/')
async def redirect_to_main_page(request: Request):
    if not validate_token(request.cookies.get('Token')):
        return RedirectResponse(
            url='/auth/login',
            status_code=status.HTTP_303_SEE_OTHER
            )

    return RedirectResponse(
        url='/main_page',
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get('/main_page')
async def main_page(request: Request):
    if not validate_token(request.cookies.get('Token')):
        return RedirectResponse(
            url='/auth/login',
            status_code=status.HTTP_303_SEE_OTHER
            )

    all_users: List[UserSchema] = await get_all_users()
    all_items: List[ItemSchema] = await get_all_items()
    return templates.TemplateResponse(name="main_page.html", context={
        "request": request,
        "all_users": all_users,
        "all_items": all_items
    })


@router.post('/main_page')
async def add_item(request: Request, item_data: AppendSchema):
    if not validate_token(request.cookies.get('Token')):
        return RedirectResponse(
            url='/auth/login',
            status_code=status.HTTP_303_SEE_OTHER
            )

    is_append = await add_new_item(item_data)
    if not is_append:
        raise HTTPException(status_code=400, detail="Ошибка :(")


@router.patch('/main_page')
async def update_item(request: Request, item_data: UpdateAndDeleteItemSchema):
    if not validate_token(request.cookies.get('Token')):
        return RedirectResponse(
            url='/auth/login',
            status_code=status.HTTP_303_SEE_OTHER
            )

    await edit_item(new_item_data=item_data)


@router.post('/main_page/delete/{item_id}')
async def delete_item(request: Request, item_id):
    if not validate_token(request.cookies.get('Token')):
        return RedirectResponse(
            url='/auth/login',
            status_code=status.HTTP_303_SEE_OTHER
            )

    await remove_item(item_id=int(item_id))
