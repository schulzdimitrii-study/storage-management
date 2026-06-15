from fastapi import FastAPI
from routes.suppliers import suppliers_router
from routes.category import categories_router
from routes.products import products_router
from routes.stock_movements import stock_movements_router
from middlewares.logging import logging_middleware
from middlewares.custom_header import add_custom_header


app = FastAPI(
    title="Storage Management API",
    description="API for managing inventory and stock movements",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.middleware("http")(logging_middleware)
app.middleware("http")(add_custom_header)

app.include_router(suppliers_router, prefix="/api/v1",)
app.include_router(categories_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(stock_movements_router, prefix="/api/v1")

@app.get("/", tags=["Healthcheck"])
def read_root():
    return {"message": "API is running! 🚀"}
