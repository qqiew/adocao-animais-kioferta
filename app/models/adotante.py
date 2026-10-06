from app.data.adotantes_mock import ADOTANTES


class Adotante:
    """Pessoa que quer adotar. Maior de idade e com limite de adoções."""

    IDADE_MINIMA = 18
    MAX_ADOCOES = 2

    def __init__(self, id, nome, idade, tem_quintal):
        self._id = id
        self._adocoes = 0
        self.alterar_nome(nome)
        self.alterar_idade(idade)
        self._tem_quintal = tem_quintal

    # --- leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_idade(self):
        return self._idade

    def mostrar_quintal(self):
        return self._tem_quintal

    def mostrar_adocoes(self):
        return self._adocoes

    # --- alteracao, com regra ---
    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome do adotante não pode ser vazio')
        self._nome = novo_nome.strip()

    def alterar_idade(self, nova_idade):
        if nova_idade < self.IDADE_MINIMA:
            raise ValueError(f'adotante precisa ter ao menos {self.IDADE_MINIMA} anos')
        self._idade = nova_idade

    # --- comportamento ---
    def pode_adotar(self):
        return self._adocoes < self.MAX_ADOCOES

    def registrar_adocao(self):
        self._adocoes += 1

    def __repr__(self):
        return f'Adotante({self._nome})'


def carregar_adotantes():
    return [Adotante(a['id'], a['nome'], a['idade'], a['tem_quintal'])
            for a in ADOTANTES]
