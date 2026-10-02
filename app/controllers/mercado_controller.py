from app.models.mercado import carregar_mercados


class MercadoController:
    def __init__(self):
        self._mercados = carregar_mercados()

    def listar(self):
        return [self._para_dicionario(m) for m in self._mercados]

    def buscar(self, id):
        for mercado in self._mercados:
            if mercado.mostrar_id() == id:
                return self._para_dicionario(mercado)
        return None

    def _para_dicionario(self, mercado):
        lat, lng = mercado.mostrar_localizacao()
        return {
            'id': mercado.mostrar_id(),
            'nome': mercado.mostrar_nome(),
            'lat': lat,
            'lng': lng,
        }
