from fastapi import Request
import time

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    print(f"➡️ {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"⬅️ {request.method} {request.url} completed in {process_time:.2f} seconds with status code {response.status_code}")
    
    return response