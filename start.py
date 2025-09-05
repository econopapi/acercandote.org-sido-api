import uvicorn
from api.main import api

if __name__ == "__main__":
    uvicorn.run(
        "api.main:api",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Reinicia automáticamente cuando cambias código
        log_level="info"
    )