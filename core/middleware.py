# File: core/middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time

RATE_LIMIT = {}  # In-memory store: {ip: [timestamp1, timestamp2, ...]}
LIMIT = 5        # Max requests
WINDOW = 60      # In seconds

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        request_times = RATE_LIMIT.get(ip, [])
        # Remove timestamps outside the window
        request_times = [t for t in request_times if now - t < WINDOW]

        if request.url.path.startswith(("/auth/login", "/wallet/fund")):  # Apply to sensitive endpoints
            if len(request_times) >= LIMIT:
                raise HTTPException(status_code=429, detail="Too many requests. Please wait.")
            request_times.append(now)

        RATE_LIMIT[ip] = request_times
        response = await call_next(request)
        return response
