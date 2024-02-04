from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Auth.jwt_handler import JWTHandler


class JwtBearer(HTTPBearer):
    __jwt_handler: JWTHandler

    def __init__(self, auto_Error: bool = True, jwt_handler: JWTHandler = JWTHandler()):
        super(JwtBearer, self).__init__(auto_error=auto_Error)
        self.__jwt_handler = jwt_handler

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Expired token")

    def verify_jwt(self, token: dict) -> bool:
        isTokenValid: bool = False
        payload = self.__jwt_handler.decode_JWT(token)
        if payload:
            isTokenValid = not isTokenValid

        return isTokenValid
