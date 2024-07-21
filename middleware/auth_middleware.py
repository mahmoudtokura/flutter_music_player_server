from fastapi import HTTPException, Header, status
import jwt


def auth_middleware(x_auth_token=Header()):
    if not x_auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required"
        )
    try:
        verified_token = jwt.decode(
            x_auth_token, "test_password_key", algorithms="HS256"
        )
        if not verified_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        uid = verified_token.get("id")
        return {"uid": uid, "token": x_auth_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
