from fastapi import FastAPI

from api.routes import auth_router, user_router, vinyl_router

app = FastAPI(
    title="Empréstimos de Vinis",
    description="API que irá servir os dados para os empréstimos",
    version="0.0.1",
)

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(vinyl_router, prefix="/api", tags=["vinyl"])


@app.get("/")
def read_root():
    return {"msg": "API FastAPI"}
