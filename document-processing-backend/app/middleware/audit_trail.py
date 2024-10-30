from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.audit_trail import AuditTrail

class AuditTrailMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        user_id = getattr(request.state, 'user', {}).get('user_id')
        print(user_id)
        action_type = request.method
        action = f"Path: {request.url.path}, Params: {request.query_params}"
        if user_id:
            db: Session = next(get_db())
            audit_entry = AuditTrail(
                user_id=int(user_id),
                action=action,
                timestamp=datetime.now(),
                action_type=action_type)
            db.add(audit_entry)
            db.commit()

        return response