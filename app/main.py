from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from repository import init_db
from router import router
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API для управления товарами",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    return JSONResponse(
        content={
            "message": "Products API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "create_product": "POST /products/",
                "get_products": "GET /products/",
                "get_product": "GET /products/{product_id}",
                "update_product": "PUT /products/{product_id}",
                "delete_product": "DELETE /products/{product_id}",
            },
        }
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.APP_VERSION,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )