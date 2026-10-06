from app.models.animal import carregar_animais


class AnimalController:
    def __init__(self):
        self._animais = carregar_animais()

    def mostrar_modelos(self):
        return self._animais

    def listar(self):
        return [self._para_dicionario(a) for a in self._animais]

    def listar_disponiveis(self):
        animais = [a for a in self._animais if a.esta_disponivel()]
        return [self._para_dicionario(a) for a in animais]

    def listar_por_especie(self, especie):
        animais = [a for a in self._animais if a.pertence_a(especie)]
        return [self._para_dicionario(a) for a in animais]

    def buscar(self, id):
        for animal in self._animais:
            if animal.mostrar_id() == id:
                return self._para_dicionario(animal)
        return None

    def _para_dicionario(self, animal):
        return {
            'id': animal.mostrar_id(),
            'nome': animal.mostrar_nome(),
            'especie': animal.mostrar_especie(),
            'idade': animal.mostrar_idade(),
            'porte': animal.mostrar_porte(),
            'descricao': animal.descricao(),
            'taxa_adocao': animal.mostrar_taxa(),
            'adotado': animal.mostrar_adotado(),
        }