from fastapi import APIRouter, HTTPException

from app.controllers.animal_controller import AnimalController

router = APIRouter(prefix='/api/animais', tags=['animais'])
controller = AnimalController()


@router.get('')
def listar():
    return controller.listar()


@router.get('/disponiveis')
def listar_disponiveis():
    return controller.listar_disponiveis()


@router.get('/especie/{especie}')
def listar_por_especie(especie: str):
    animais = controller.listar_por_especie(especie)
    if not animais:
        raise HTTPException(404, 'nenhum animal dessa espécie')
    return animais


@router.get('/{id}')
def buscar(id: int):
    animal = controller.buscar(id)
    if animal is None:
        raise HTTPException(404, 'animal não encontrado')
    return animal
