from fastapi import APIRouter, HTTPException

from app.controllers.mercado_controller import MercadoController
from app.controllers.oferta_controller import OfertaController

router = APIRouter(prefix='/api/mercados', tags=['mercados'])
controller = MercadoController()
ofertas = OfertaController()


@router.get('')
def listar():
    return controller.listar()


@router.get('/{id}')
def buscar(id: int):
    mercado = controller.buscar(id)
    if mercado is None:
        raise HTTPException(404, 'mercado não encontrado')
    return mercado


@router.get('/{id}/ofertas')
def ofertas_do_mercado(id: int):
    if controller.buscar(id) is None:
        raise HTTPException(404, 'mercado não encontrado')
    return ofertas.listar_por_mercado(id)
