from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            if(e):
                message = str(e)
            else: 
                message = "Internal Server Error"
            return JSONResponse(status_code=500, content={"message": message})
