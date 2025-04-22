# File: core/middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time

# === Settings ===
RATE_LIMITS = {
    "/auth/login": {"limit": 5, "window": 60},           # 5 requests per 60 seconds
    "/wallet/fund": {"limit": 3, "window": 60},          # 3 requests per 60 seconds
    "/disputes/submit": {"limit": 3, "window": 120},     # 3 disputes per 2 minutes
    "/kyc/upload-file": {"limit": 2, "window": 300},     # 2 uploads per 5 minutes
}

RATE_TRACKER = {}  # Structure: {ip: {path: [timestamps]}}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        path = request.url.path

        # Match the start of the path with configured routes
        for route, config in RATE_LIMITS.items():
            if path.startswith(route):
                now = time.time()
                tracker = RATE_TRACKER.get(ip, {}).get(route, [])
                tracker = [t for t in tracker if now - t < config["window"]]

                if len(tracker) >= config["limit"]:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Try again in {int(config['window'])} seconds."
                    )

                tracker.append(now)
                RATE_TRACKER.setdefault(ip, {})[route] = tracker
                break  # Only apply to the first matching route

        response = await call_next(request)
        return response
