"""Verificacao do modelo de referencia.

Roda sem subir a API: testa as models e os controllers.
Use este arquivo como molde para verificar o seu proprio modulo.
"""
from app.models.usuario import (Usuario, Visitante, Contribuidor,
                                Moderador, carregar_usuarios)
from app.models.produto import Produto, carregar_produtos
from app.models.mercado import Mercado, carregar_mercados
from app.models.oferta import Oferta, carregar_ofertas

falhas = 0


def checar(ok, descricao):
    global falhas
    if ok:
        print(f'  ok      {descricao}')
    else:
        print(f'  FALHOU  {descricao}')
        falhas += 1


print('\n1. Encapsulamento: o objeto nasce valido')
try:
    Produto(99, '   ', 'Teste', 10)
    checar(False, 'deveria recusar nome vazio no construtor')
except ValueError:
    checar(True, 'construtor recusa nome vazio')
try:
    Produto(99, 'Teste', 'Teste', -1)
    checar(False, 'deveria recusar preco negativo no construtor')
except ValueError:
    checar(True, 'construtor recusa preco negativo')
checar(not hasattr(Produto, 'alterar_id'), 'nao existe alterar_id')

print('\n2. Encapsulamento: Mercado valida coordenadas')
try:
    Mercado(99, 'Teste', 500, 0)
    checar(False, 'deveria recusar latitude 500')
except ValueError:
    checar(True, 'construtor recusa latitude invalida')

print('\n3. Heranca: a hierarquia esta correta')
checar(issubclass(Visitante, Usuario), 'Visitante herda de Usuario')
checar(issubclass(Contribuidor, Visitante), 'Contribuidor herda de Visitante')
checar(issubclass(Moderador, Contribuidor), 'Moderador herda de Contribuidor')

print('\n4. Heranca: cada filha escreve so a diferenca')
checar('mostrar_permissoes' in Contribuidor.__dict__,
       'Contribuidor sobrescreve mostrar_permissoes')
checar('verificar_senha' not in Moderador.__dict__,
       'Moderador NAO reescreve verificar_senha: herda')

print('\n5. Polimorfismo: a mesma chamada, respostas diferentes')
usuarios = carregar_usuarios()
bia, ana, caio = usuarios
checar([type(u).__name__ for u in usuarios] ==
       ['Visitante', 'Contribuidor', 'Moderador'],
       'o mock virou tres classes diferentes')
checar(len(bia.mostrar_permissoes()) == 1, 'Visitante tem 1 permissao')
checar(len(ana.mostrar_permissoes()) == 2, 'Contribuidor tem 2 permissoes')
checar(len(caio.mostrar_permissoes()) == 4, 'Moderador tem 4 permissoes')
checar(caio.pode('cadastrar_oferta'),
       'Moderador herdou a permissao do Contribuidor')
checar(not bia.pode('remover_oferta'), 'Visitante nao pode moderar')

print('\n6. Seguranca: a senha nao vaza')
checar(not hasattr(Usuario, 'mostrar_senha'), 'nao existe mostrar_senha')
checar(bia.verificar_senha('bia123'), 'senha correta e aceita')
checar(not bia.verificar_senha('errada'), 'senha errada e recusada')

print('\n7. Associacao: a oferta guarda objetos, nao ids')
ofertas = carregar_ofertas()
primeira = ofertas[0]
checar(isinstance(primeira.mostrar_produto(), Produto),
       'mostrar_produto devolve um Produto')
checar(isinstance(primeira.mostrar_mercado(), Mercado),
       'mostrar_mercado devolve um Mercado')
checar(primeira.mostrar_produto().mostrar_nome() == 'Arroz Tipo 1 5kg',
       'o encadeamento chega ao nome do produto')

print('\n8. Regra que depende da associacao')
produto = primeira.mostrar_produto()
mercado = primeira.mostrar_mercado()
try:
    Oferta(99, produto, mercado, produto.mostrar_preco() + 1)
    checar(False, 'deveria recusar oferta mais cara que o preco normal')
except ValueError:
    checar(True, 'recusa oferta que nao e mais barata')

print('\n9. A conta mora no objeto')
checar(primeira.economia() == 5.0, 'economia calculada pela propria oferta')
checar(primeira.desconto_percentual() == 20.1, 'desconto percentual correto')

print('\n10. Colecoes: filtrar e ordenar')
from app.controllers.oferta_controller import OfertaController
oc = OfertaController()
comp = oc.comparativo(1)
checar(comp is not None, 'o produto 1 tem comparativo')
checar(comp['mercados'] == 3, 'o arroz aparece em tres mercados')
precos = [o['preco'] for o in comp['ofertas']]
checar(precos == sorted(precos), 'as ofertas saem ordenadas pelo preco')
checar(comp['menor_preco'] == 19.9, 'o menor preco e o primeiro da lista')
checar(oc.comparativo(6) is None, 'produto sem oferta devolve None')

print('\n11. Camadas: a model nao conhece o FastAPI')
import app.models.produto as mp
import app.models.usuario as mu
import app.models.oferta as mo
for modulo in (mp, mu, mo):
    conteudo = open(modulo.__file__, encoding='utf-8').read()
    checar('fastapi' not in conteudo,
           f'{modulo.__name__.split(".")[-1]}.py nao importa fastapi')

print('\n12. Camadas: o controller nao devolve codigo HTTP')
import app.controllers.oferta_controller as co
conteudo = open(co.__file__, encoding='utf-8').read()
checar('HTTPException' not in conteudo,
       'oferta_controller.py nao usa HTTPException')

print()
if falhas == 0:
    print('TUDO CERTO. Agora suba a API e teste no /docs.')
else:
    print(f'{falhas} verificacao(oes) falharam.')
