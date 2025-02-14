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

access_forbidden_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Access forbidden'
)

login_in_use_exc = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Login is already in use'
)


not_null_violation_exc = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Cannot explicitly set null in patch request'
)


user_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='User not found'
)

