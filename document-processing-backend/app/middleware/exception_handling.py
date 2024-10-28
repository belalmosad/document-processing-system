from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            if(e):
                message = str(e.detail)
                status_code = e.status_code
            else: 
                message = "Internal Server Error"
                status_code = 500
            return JSONResponse(status_code=status_code, content={"message": message})
