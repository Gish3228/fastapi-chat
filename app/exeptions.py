from fastapi import HTTPException, status


invalid_token_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

invalid_credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

login_in_use_exc = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Login is already in use')

