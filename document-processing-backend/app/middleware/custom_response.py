import json
import time
from typing import AsyncGenerator
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

class CustomResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        if isinstance(response.body_iterator, AsyncGenerator):
            response.headers["X-Process-Time"] = f"{(time.time() - start_time) * 1000:.2f} ms"
            return response
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        try:
            parsed_body = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            parsed_body = body.decode("utf-8")
        process_time = time.time() - start_time
        return JSONResponse(
           content={
                "status": response.status_code,
                "data": parsed_body if body else None,
                "process_time": f"{process_time * 1000} ms"
           },
           status_code=200
        )