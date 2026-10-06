from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.adocao_routes import router as adocao_router
from app.routes.animal_routes import router as animal_router

app = FastAPI(title='Adoção de Animais API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(animal_router)
app.include_router(adocao_router)


@app.get('/')
def raiz():
    return {'api': 'Adoção de Animais', 'docs': '/docs'}
