import time
import jwt
from decouple import config


class JWTHandler:
    JWT_SECRET = config("secret")
    JWT_ALGORITHM = config("algorithm")
    x = 5

    def __token_response(self, token: str) -> dict:
        return {
            "access_token": token
        }

    def register_jwt(self, user_id: str) -> dict:
        payload = {
            "userID": user_id,
            "expiry": time.time() + 1200
        }
        token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
        return self.__token_response(token)

    def decode_JWT(self, token: dict) -> dict:
        try:
            decode_token = jwt.decode(token["access_token"], self.JWT_SECRET, self.JWT_ALGORITHM)
            return decode_token if decode_token["expiry"] >= time.time() else {"error": "Token expired"}
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}
