from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.produto_routes import router as produto_router
from app.routes.usuario_routes import router as usuario_router
from app.routes.mercado_routes import router as mercado_router
from app.routes.oferta_routes import router as oferta_router

app = FastAPI(title='KiOferta API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(produto_router)
app.include_router(usuario_router)
app.include_router(mercado_router)
app.include_router(oferta_router)


@app.get('/')
def raiz():
    return {'api': 'KiOferta', 'docs': '/docs'}
