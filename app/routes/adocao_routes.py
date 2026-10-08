from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.adocao_controller import AdocaoController
from app.models.erros import ConflitoError
from app.routes.animal_routes import controller as animal_controller

router = APIRouter(prefix='/api', tags=['adocoes'])
controller = AdocaoController(animal_controller.mostrar_modelos())


class AdocaoRequest(BaseModel):
    animal_id: int
    adotante_id: int
    data: Optional[str] = None


@router.post('/adocoes', status_code=201)
def registrar(dados: AdocaoRequest):
    try:
        adocao = controller.registrar(dados.animal_id, dados.adotante_id, dados.data)
    except ConflitoError as erro:
        raise HTTPException(409, str(erro))
    except ValueError as erro:
        raise HTTPException(422, str(erro))
    if adocao is None:
        raise HTTPException(404, 'animal ou adotante não encontrado')
    return adocao


@router.get('/adotantes/{id}/adocoes')
def listar_por_adotante(id: int):
    adocoes = controller.listar_por_adotante(id)
    if adocoes is None:
        raise HTTPException(404, 'adotante não encontrado')
    return adocoes


@router.get('/relatorio/taxas')
def relatorio_taxas():
    return controller.total_taxas()
