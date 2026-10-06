from app.data.animais_mock import ANIMAIS
from app.models.erros import ConflitoError

PORTES = ('pequeno', 'medio', 'grande')


class Animal:
    """Um animal do abrigo. A espécie e a taxa de adoção vêm das filhas."""

    ESPECIE = 'animal'
    TAXA_ADOCAO = 0.0

    def __init__(self, id, nome, idade, porte):
        self._id = id
        self._adotado = False
        self.alterar_nome(nome)
        self.alterar_idade(idade)
        self.alterar_porte(porte)

    # --- leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_idade(self):
        return self._idade

    def mostrar_porte(self):
        return self._porte

    def mostrar_especie(self):
        return self.ESPECIE

    def mostrar_taxa(self):
        return self.TAXA_ADOCAO

    def mostrar_adotado(self):
        return self._adotado

    # --- alteracao, com regra ---
    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome do animal não pode ser vazio')
        self._nome = novo_nome.strip()

    def alterar_idade(self, nova_idade):
        if nova_idade < 0 or nova_idade > 30:
            raise ValueError('idade do animal deve estar entre 0 e 30')
        self._idade = nova_idade

    def alterar_porte(self, novo_porte):
        if novo_porte not in PORTES:
            raise ValueError('porte deve ser pequeno, medio ou grande')
        self._porte = novo_porte

    # --- comportamento ---
    def esta_disponivel(self):
        return not self._adotado

    def descricao(self):
        return f'{self._nome}, {self._idade} ano(s), porte {self._porte}'

    def verificar_adotante(self, adotante):
        if not self.esta_disponivel():
            raise ConflitoError('animal já foi adotado')
        if not adotante.pode_adotar():
            raise ConflitoError('adotante atingiu o limite de adoções')

    def marcar_adotado(self):
        self._adotado = True

    def pertence_a(self, especie):
        return self.ESPECIE == especie.strip().lower()

    def __repr__(self):
        return f'{self.__class__.__name__}({self._nome})'


class Cao(Animal):
    """Cão: taxa maior e exige quintal quando o porte é grande."""

    ESPECIE = 'cao'
    TAXA_ADOCAO = 80.0

    def descricao(self):
        return super().descricao() + ' - precisa de passeios diários'

    def verificar_adotante(self, adotante):
        super().verificar_adotante(adotante)
        if self._porte == 'grande' and not adotante.mostrar_quintal():
            raise ValueError('cão de porte grande exige adotante com quintal')


class Gato(Animal):
    """Gato: taxa menor, sem exigências extras."""

    ESPECIE = 'gato'
    TAXA_ADOCAO = 50.0

    def descricao(self):
        return super().descricao() + ' - ideal para apartamento'


# O mock guarda a espécie como texto; o valor do dicionário é a própria classe.
ESPECIES = {
    'cao': Cao,
    'gato': Gato,
}


def carregar_animais():
    return [ESPECIES[a['especie']](a['id'], a['nome'], a['idade'], a['porte'])
            for a in ANIMAIS]
