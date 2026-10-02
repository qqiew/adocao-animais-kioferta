from app.data.usuarios_mock import USUARIOS


class Usuario:
    """Classe base. As filhas mudam apenas o que podem fazer."""

    def __init__(self, id, nome, senha):
        self._id = id
        self.alterar_nome(nome)
        self._senha = senha

    # --- leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_perfil(self):
        return self.__class__.__name__.lower()

    # nao existe mostrar_senha: a senha so pode ser conferida
    def verificar_senha(self, senha):
        return self._senha == senha

    # --- alteracao, com regra ---
    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome não pode ser vazio')
        self._nome = novo_nome.strip()

    # --- polimorfismo: cada filha responde do seu jeito ---
    def mostrar_permissoes(self):
        return []

    def pode(self, acao):
        return acao in self.mostrar_permissoes()

    def __repr__(self):
        return f'{self.__class__.__name__}({self._nome})'


class Visitante(Usuario):
    def mostrar_permissoes(self):
        return ['ver_ofertas']


class Contribuidor(Visitante):
    def mostrar_permissoes(self):
        return super().mostrar_permissoes() + ['cadastrar_oferta']


class Moderador(Contribuidor):
    def mostrar_permissoes(self):
        return super().mostrar_permissoes() + ['remover_oferta', 'banir_usuario']


# o valor do dicionario e a propria CLASSE, nao um texto
PERFIS = {
    'visitante': Visitante,
    'contribuidor': Contribuidor,
    'moderador': Moderador,
}


def carregar_usuarios():
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])
            for u in USUARIOS]
