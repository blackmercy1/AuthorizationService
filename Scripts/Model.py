from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    jwt_access_token: dict = Field(default=None)
    jwt_refresh_token: dict = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "email": "help@hello.gmail.com",
                "password": "1234"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    login_schema: UserLoginSchema = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "fullname": "Selim",
                "email": "help@hello.gmail.com",
                "password": "1234"
            }
        }
