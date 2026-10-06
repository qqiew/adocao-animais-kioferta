from app.data.adocoes_mock import ADOCOES
from app.models.adotante import carregar_adotantes
from app.models.animal import carregar_animais


class Adocao:
    """A adoção de um Animal por um Adotante.

    Associacao: a adoção guarda os OBJETOS Animal e Adotante, nao os ids.
    """

    def __init__(self, id, animal, adotante, data):
        self._id = id
        self._animal = animal
        self._adotante = adotante
        self.alterar_data(data)
        animal.verificar_adotante(adotante)
        animal.marcar_adotado()
        adotante.registrar_adocao()

    # --- leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_animal(self):
        return self._animal

    def mostrar_adotante(self):
        return self._adotante

    def mostrar_data(self):
        return self._data

    # --- alteracao, com regra ---
    def alterar_data(self, nova_data):
        if nova_data.strip() == '':
            raise ValueError('data da adoção não pode ser vazia')
        self._data = nova_data.strip()

    # --- comportamento ---
    def e_do_adotante(self, adotante_id):
        return self._adotante.mostrar_id() == adotante_id

    def valor_taxa(self):
        return self._animal.mostrar_taxa()

    def __repr__(self):
        return (f'Adocao({self._animal.mostrar_nome()} '
                f'por {self._adotante.mostrar_nome()})')


def carregar_adocoes(animais=None, adotantes=None):
    """Transforma os ids do mock em referencias para os objetos reais.

    Recebe as listas ja carregadas para que a adoção marque os MESMOS objetos
    que o controller de animais usa; sem argumentos, carrega listas novas.
    """
    animais = animais if animais is not None else carregar_animais()
    adotantes = adotantes if adotantes is not None else carregar_adotantes()
    animais_por_id = {a.mostrar_id(): a for a in animais}
    adotantes_por_id = {a.mostrar_id(): a for a in adotantes}

    adocoes = []
    for d in ADOCOES:
        adocoes.append(Adocao(
            d['id'],
            animais_por_id[d['animal_id']],
            adotantes_por_id[d['adotante_id']],
            d['data'],
        ))
    return adocoes
