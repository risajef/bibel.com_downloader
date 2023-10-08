from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers.download.router import router as download_router
from controllers.setup import router as setup_router
from controllers.data.router import router as data_router
from controllers.swagger import router as swagger_router
from controllers.frontend.router import router as frontend_router

# Define your database models using SQLAlchemy

app = FastAPI(title="Bible Analytics", version="0.0.2", docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(data_router)
app.include_router(download_router)
app.include_router(setup_router)
app.include_router(frontend_router)

app.include_router(swagger_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)