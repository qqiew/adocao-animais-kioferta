from fastapi import APIRouter, HTTPException

from app.controllers.oferta_controller import OfertaController

router = APIRouter(prefix='/api', tags=['ofertas'])
controller = OfertaController()


@router.get('/ofertas')
def listar():
    return controller.listar()


@router.get('/ofertas/{id}')
def buscar(id: int):
    oferta = controller.buscar(id)
    if oferta is None:
        raise HTTPException(404, 'oferta não encontrada')
    return oferta


@router.get('/produtos/{produto_id}/ofertas')
def ofertas_do_produto(produto_id: int):
    ofertas = controller.listar_por_produto(produto_id)
    if not ofertas:
        raise HTTPException(404, 'nenhuma oferta para este produto')
    return ofertas


@router.get('/produtos/{produto_id}/comparativo')
def comparativo(produto_id: int):
    dados = controller.comparativo(produto_id)
    if dados is None:
        raise HTTPException(404, 'nenhuma oferta para este produto')
    return dados
