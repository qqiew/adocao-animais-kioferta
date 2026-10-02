from app.models.oferta import carregar_ofertas


class OfertaController:
    def __init__(self):
        self._ofertas = carregar_ofertas()

    def listar(self):
        return [self._para_dicionario(o) for o in self._ofertas]

    def buscar(self, id):
        for oferta in self._ofertas:
            if oferta.mostrar_id() == id:
                return self._para_dicionario(oferta)
        return None

    def listar_por_produto(self, produto_id):
        do_produto = [o for o in self._ofertas if o.e_do_produto(produto_id)]
        ordenadas = sorted(do_produto, key=lambda o: o.mostrar_preco())
        return [self._para_dicionario(o) for o in ordenadas]

    def listar_por_mercado(self, mercado_id):
        do_mercado = [o for o in self._ofertas if o.e_do_mercado(mercado_id)]
        ordenadas = sorted(do_mercado, key=lambda o: o.mostrar_preco())
        return [self._para_dicionario(o) for o in ordenadas]

    def comparativo(self, produto_id):
        do_produto = [o for o in self._ofertas if o.e_do_produto(produto_id)]
        if not do_produto:
            return None

        ordenadas = sorted(do_produto, key=lambda o: o.mostrar_preco())
        melhor = ordenadas[0]
        produto = melhor.mostrar_produto()

        return {
            'produto': produto.mostrar_nome(),
            'preco_normal': produto.mostrar_preco(),
            'menor_preco': melhor.mostrar_preco(),
            'economia': melhor.economia(),
            'mercados': len(ordenadas),
            'ofertas': [self._para_dicionario(o) for o in ordenadas],
        }

    def _para_dicionario(self, oferta):
        return {
            'id': oferta.mostrar_id(),
            'produto': oferta.mostrar_produto().mostrar_nome(),
            'mercado': oferta.mostrar_mercado().mostrar_nome(),
            'preco': oferta.mostrar_preco(),
            'economia': oferta.economia(),
            'desconto': oferta.desconto_percentual(),
        }
