from app.data.ofertas_mock import OFERTAS
from app.models.mercado import carregar_mercados
from app.models.produto import carregar_produtos


class Oferta:
    """O preco promocional de um Produto em um Mercado.

    Associacao: a oferta guarda os OBJETOS Produto e Mercado, nao os ids.
    """

    def __init__(self, id, produto, mercado, novo_preco):
        self._id = id
        self._produto = produto
        self._mercado = mercado
        self.alterar_preco(novo_preco)

    # --- leitura ---
    def mostrar_id(self):
        return self._id

    def mostrar_produto(self):
        return self._produto

    def mostrar_mercado(self):
        return self._mercado

    def mostrar_preco(self):
        return self._novo_preco

    # --- alteracao, com regra ---
    def alterar_preco(self, novo_preco):
        if novo_preco <= 0:
            raise ValueError('preço da oferta precisa ser maior que zero')
        if novo_preco >= self._produto.mostrar_preco():
            raise ValueError('oferta precisa ser mais barata que o preço normal')
        self._novo_preco = novo_preco

    # --- comportamento ---
    def e_do_produto(self, produto_id):
        return self._produto.mostrar_id() == produto_id

    def e_do_mercado(self, mercado_id):
        return self._mercado.mostrar_id() == mercado_id

    def economia(self):
        return round(self._produto.mostrar_preco() - self._novo_preco, 2)

    def desconto_percentual(self):
        normal = self._produto.mostrar_preco()
        return round(self.economia() / normal * 100, 1)

    def __repr__(self):
        return (f'Oferta({self._produto.mostrar_nome()} '
                f'no {self._mercado.mostrar_nome()})')


def carregar_ofertas():
    """Transforma os ids do mock em referencias para os objetos reais.

    E o que um banco de dados faria com um JOIN.
    """
    produtos = {p.mostrar_id(): p for p in carregar_produtos()}
    mercados = {m.mostrar_id(): m for m in carregar_mercados()}

    ofertas = []
    for o in OFERTAS:
        ofertas.append(Oferta(
            o['id'],
            produtos[o['produto_id']],
            mercados[o['mercado_id']],
            o['preco'],
        ))
    return ofertas
