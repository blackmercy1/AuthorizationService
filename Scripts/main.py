from typing import List, Optional

import uvicorn
from fastapi import FastAPI, Body, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from Auth.jwt_bearer import JwtBearer
from Auth.jwt_handler import JWTHandler
from Scripts.Model import UserLoginSchema, UserSchema
from logger import Logger

app = FastAPI()
jwt_handler = JWTHandler()
jwt_bearer = JwtBearer(jwt_handler=jwt_handler)
logger = Logger()
templates = Jinja2Templates(directory="html")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

users: List[UserSchema] = []


@app.get("/user/signup", response_class=FileResponse, tags=["signup"])
async def show_sign_up_form() -> FileResponse:
    return FileResponse("/Users/black_mercy/PycharmProjects/FastAPILearn/html/Sign.html")


@app.post("/user/signup/", tags=["signup"])
def sign_up(username: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    new_user = UserSchema()
    new_user.login_schema = UserLoginSchema(email=username, password=password)
    if check_user(new_user.login_schema) is None:
        new_user.login_schema.jwt_access_token = jwt_handler.register_jwt(new_user.login_schema.email)
        users.append(new_user)
        return RedirectResponse(url="/user/login")
    else:
        logger.logger.error("You are already signed up")
        return RedirectResponse(url="/user/error")


def check_user(user: UserLoginSchema) -> Optional[UserSchema]:
    for user_data in users:
        if user_data.login_schema.email == user.email and user_data.login_schema.password == user.password:
            return user_data
    return None


def check_user_tokens(jwt_access_token: dict) -> bool:
    return jwt_bearer.verify_jwt(jwt_access_token)


def log(user: UserLoginSchema = Body(default=None)) -> dict:
    if check_user(user):
        return jwt_handler.register_jwt(user.email)
    else:
        return {"error": "User not found, try to sign up first of all"}


@app.get("/user/login/", tags=["users"], response_class=FileResponse)
async def show_authorization_form() -> FileResponse:
    return FileResponse("/Users/black_mercy/PycharmProjects/FastAPILearn/html/authorization.html")


@app.post("/user/login/", tags=["users"])
def try_to_login(username: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    user = check_user(UserLoginSchema(email=username, password=password))
    if user is not None:
        if check_user_tokens(user.login_schema.jwt_access_token):
            return RedirectResponse(url="/main")

    else:
        logger.logger.error("User not found sign up first of all")
        return RedirectResponse(url="/user/error")
    return RedirectResponse(url="/user/error")
