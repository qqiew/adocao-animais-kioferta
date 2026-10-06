from datetime import date

from app.models.adocao import Adocao, carregar_adocoes
from app.models.adotante import carregar_adotantes


class AdocaoController:
    def __init__(self, animais):
        self._animais = animais
        self._adotantes = carregar_adotantes()
        self._adocoes = carregar_adocoes(self._animais, self._adotantes)

    def registrar(self, animal_id, adotante_id, data=None):
        animal = self._achar(self._animais, animal_id)
        adotante = self._achar(self._adotantes, adotante_id)
        if animal is None or adotante is None:
            return None
        data = data if data is not None else date.today().isoformat()
        adocao = Adocao(len(self._adocoes) + 1, animal, adotante, data)
        self._adocoes.append(adocao)
        return self._para_dicionario(adocao)

    def listar_por_adotante(self, adotante_id):
        if self._achar(self._adotantes, adotante_id) is None:
            return None
        adocoes = [a for a in self._adocoes if a.e_do_adotante(adotante_id)]
        return [self._para_dicionario(a) for a in adocoes]

    def total_taxas(self):
        return {
            'adocoes': len(self._adocoes),
            'total_taxas': sum(a.valor_taxa() for a in self._adocoes),
        }

    def _achar(self, itens, id):
        for item in itens:
            if item.mostrar_id() == id:
                return item
        return None

    def _para_dicionario(self, adocao):
        return {
            'id': adocao.mostrar_id(),
            'animal': adocao.mostrar_animal().mostrar_nome(),
            'adotante': adocao.mostrar_adotante().mostrar_nome(),
            'data': adocao.mostrar_data(),
            'taxa': adocao.valor_taxa(),
        }