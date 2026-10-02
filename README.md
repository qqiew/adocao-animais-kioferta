# KiOferta API — repositório modelo

Backend de referência da disciplina de **Programação Orientada a Objetos**.
Construído em quatro camadas, no padrão **MVC**, com FastAPI.

Este repositório é o **modelo**: use a estrutura, os nomes e os padrões daqui
para construir o sistema da sua equipe.

---

## Como rodar

```bash
# 1. clonar e entrar na pasta
git clone https://github.com/faustinopsy/kioferta-python.git
cd kioferta-python

# 2. criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux e macOS

# 3. instalar as bibliotecas
pip install -r requirements.txt

# 4. subir a API
uvicorn main:app --reload
```

Abra `http://127.0.0.1:8000/docs`.

---

## Verificar se está tudo certo

```bash
python verificar.py        # testa models e controllers, sem subir a API
python testar_rotas.py     # testa as 24 rotas (precisa de: pip install httpx)
```

Os dois scripts são o molde do que será exigido na sua entrega.

---

## A estrutura

```
kioferta-api/
├── main.py                  liga os módulos à aplicação
├── requirements.txt
├── verificar.py             testa models e controllers
├── testar_rotas.py          testa as rotas
└── app/
    ├── data/                dados provisórios (mock)
    │   ├── produtos_mock.py
    │   ├── usuarios_mock.py
    │   ├── mercados_mock.py
    │   └── ofertas_mock.py
    ├── models/              M — classes e regras de negócio
    │   ├── produto.py       Produto + carregar_produtos()
    │   ├── mercado.py       Mercado + carregar_mercados()
    │   ├── oferta.py        Oferta  + carregar_ofertas()
    │   └── usuario.py       Usuario + 3 filhas + PERFIS + carregar_usuarios()
    ├── controllers/         C — casos de uso
    │   ├── produto_controller.py
    │   ├── usuario_controller.py
    │   ├── mercado_controller.py
    │   └── oferta_controller.py
    └── routes/              V — endereços HTTP e códigos de resposta
        ├── produto_routes.py
        ├── usuario_routes.py
        ├── mercado_routes.py
        └── oferta_routes.py
```

### A regra de dependência

```
main.py  →  routes/  →  controllers/  →  models/  →  data/
```

A seta aponta **só para baixo**. A camada de fora conhece a de dentro; a de
dentro nunca conhece a de fora.

**Teste prático:** abra qualquer arquivo de `models/`. Se aparecer a palavra
`fastapi`, `HTTPException` ou `router`, a camada foi violada.

---

## Quem decide o quê

| Pergunta | Camada | Como |
|---|---|---|
| O nome pode ser vazio? | model | `raise ValueError` |
| O produto 99 existe? | controller | devolve `None` |
| Em que ordem as ofertas saem? | controller | `sorted` com `key` |
| Que código HTTP responder? | routes | `404`, `409`, `422` |
| Qual o endereço da rota? | routes | `APIRouter(prefix=...)` |
| De onde vêm os dados? | data | o arquivo `*_mock.py` |

---

## Os padrões que você deve copiar

### 1. Model: atributo protegido, construtor que valida

```python
class Produto:
    def __init__(self, id, nome, categoria, preco):
        self._id = id                    # protegido
        self._categoria = categoria
        self.alterar_nome(nome)          # passa pelo método, valida
        self.alterar_preco(preco)

    def mostrar_nome(self):              # leitura
        return self._nome

    def alterar_preco(self, novo_preco): # alteração com regra
        if novo_preco < 0:
            raise ValueError('preço não pode ser negativo')
        self._preco = novo_preco
```

Não existe `alterar_id`: identidade não muda.

### 2. Função de carga no fim do arquivo, fora da classe

```python
def carregar_produtos():
    return [Produto(p['id'], p['nome'], p['categoria'], p['preco'])
            for p in PRODUTOS]
```

### 3. Associação: guardar o objeto, não o id

```python
class Oferta:
    def __init__(self, id, produto, mercado, novo_preco):
        self._produto = produto   # o objeto Produto inteiro
        self._mercado = mercado   # o objeto Mercado inteiro
```

E a ligação é feita uma vez só, no carregamento:

```python
produtos = {p.mostrar_id(): p for p in carregar_produtos()}
# ...
produtos[o['produto_id']]     # o id vira objeto
```

### 4. Herança: a filha escreve só a diferença

```python
class Visitante(Usuario):
    def mostrar_permissoes(self):
        return ['ver_ofertas']

class Contribuidor(Visitante):
    def mostrar_permissoes(self):
        return super().mostrar_permissoes() + ['cadastrar_oferta']
```

`super()` **estende** a lista da classe de cima em vez de substituí-la.

### 5. Polimorfismo: nenhum `if` de perfil

```python
PERFIS = {'visitante': Visitante,
          'contribuidor': Contribuidor,
          'moderador': Moderador}

def carregar_usuarios():
    return [PERFIS[u['perfil']](u['id'], u['nome'], u['senha'])
            for u in USUARIOS]
```

O valor do dicionário é a própria **classe**. Os parênteses depois a instanciam.

### 6. Controller: filtra, ordena, converte

```python
def listar_por_produto(self, produto_id):
    do_produto = [o for o in self._ofertas if o.e_do_produto(produto_id)]
    ordenadas = sorted(do_produto, key=lambda o: o.mostrar_preco())
    return [self._para_dicionario(o) for o in ordenadas]
```

Nenhuma validação e nenhum código HTTP aqui.

### 7. Routes: traduz o resultado em resposta

```python
@router.get('/{id}')
def buscar(id: int):
    produto = controller.buscar(id)
    if produto is None:
        raise HTTPException(404, 'produto não encontrado')
    return produto
```

### 8. Acrescentar um módulo: duas linhas no main.py

```python
from app.routes.meu_routes import router as meu_router
app.include_router(meu_router)
```

---

## As 24 rotas

| Verbo | Endereço | Devolve |
|---|---|---|
| GET | `/api/produtos` | todos os produtos |
| GET | `/api/produtos/{id}` | um produto, ou 404 |
| GET | `/api/produtos/categoria/{categoria}` | produtos da categoria, ou 404 |
| GET | `/api/produtos/{id}/ofertas` | ofertas do produto, da mais barata |
| GET | `/api/produtos/{id}/comparativo` | comparativo completo, ou 404 |
| GET | `/api/mercados` | todos os mercados |
| GET | `/api/mercados/{id}` | um mercado, ou 404 |
| GET | `/api/mercados/{id}/ofertas` | ofertas daquele mercado |
| GET | `/api/ofertas` | todas as ofertas |
| GET | `/api/ofertas/{id}` | uma oferta, ou 404 |
| POST | `/api/login` | perfil e permissões, ou 401 |

---

## Exemplo de resposta

```
GET /api/produtos/1/comparativo
```

```json
{
  "produto": "Arroz Tipo 1 5kg",
  "preco_normal": 24.9,
  "menor_preco": 19.9,
  "economia": 5.0,
  "mercados": 3,
  "ofertas": [
    {"id": 1, "produto": "Arroz Tipo 1 5kg", "mercado": "Mercado Silva",
     "preco": 19.9, "economia": 5.0, "desconto": 20.1},
    {"id": 3, "produto": "Arroz Tipo 1 5kg", "mercado": "Mercadinho Bom Preço",
     "preco": 21.0, "economia": 3.9, "desconto": 15.7},
    {"id": 2, "produto": "Arroz Tipo 1 5kg", "mercado": "Supermercado Dia",
     "preco": 22.5, "economia": 2.4, "desconto": 9.6}
  ]
}
```

```
POST /api/login   { "nome": "caio", "senha": "caio123" }
```

```json
{
  "id": 3,
  "nome": "caio",
  "perfil": "moderador",
  "permissoes": ["ver_ofertas", "cadastrar_oferta",
                 "remover_oferta", "banir_usuario"]
}
```

A senha nunca aparece na resposta. Não existe `mostrar_senha`.

---

## Usuários de teste

| nome | senha | perfil | permissões |
|---|---|---|---|
| bia | bia123 | visitante | 1 |
| ana | ana123 | contribuidor | 2 |
| caio | caio123 | moderador | 4 |

---

## Erros comuns

| Sintoma | Causa | Correção |
|---|---|---|
| `ModuleNotFoundError: app` | rodou de dentro de uma subpasta | `uvicorn` a partir da raiz |
| `ModuleNotFoundError: fastapi` | ambiente virtual desativado | ative o `.venv` |
| rota não aparece no `/docs` | faltou `include_router` | duas linhas no `main.py` |
| `ImportError: circular import` | model importando controller | apague o import da model |
| `Unable to serialize` | devolveu o objeto | use `_para_dicionario` |
| erro 500 em vez de 422 | faltou `try/except` na rota | capture `ValueError` |
