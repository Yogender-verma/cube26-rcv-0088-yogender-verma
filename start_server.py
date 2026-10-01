import uvicorn
import os
import sys

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")
    print("===============================================================")
    print(f" Starting Cube 01 · Receiving Manager Backend (Host {host}, Port {port})")
    print(" Tenancy RLS: ENABLED AND FORCED")
    print(" Single-Pass Batch Vision Model: ACTIVE")
    print("===============================================================")
    uvicorn.run("backend.app:app", host=host, port=port, reload=False if os.environ.get("PORT") else True)
