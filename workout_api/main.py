# workout_api/main.py (VERSÃO ATUALIZADA)

from fastapi import FastAPI
from workout_api.routers import api_router
from fastapi_pagination import add_pagination # Importe

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)
add_pagination(app) # Adicione esta linha
