from fastapi import HTTPException, status

http_forbidden_exception: HTTPException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden."
)

http_unauth_exception: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect auth data.",
)
