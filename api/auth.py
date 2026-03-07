import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pathlib import Path
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv(Path(__file__).parent.parent / ".env")

JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verificar_credenciales(username: str, password: str) -> bool:
    return (
        username == os.getenv("API_USER") and
        password == os.getenv("API_PASSWORD")
    )


def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    return jwt.encode({"sub": username, "exp": expira}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    credencial_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credencial_error
        return username
    except JWTError:
        raise credencial_error
