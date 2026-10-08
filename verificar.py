"""Verificacao do sistema de Adocao de Animais.

Roda sem subir a API: testa as models e os controllers.
Segue o molde do verificar.py do repositorio KiOferta.
"""
import ast
import pathlib

from app.data.animais_mock import ANIMAIS
from app.models.adocao import Adocao, carregar_adocoes
from app.models.adotante import Adotante, carregar_adotantes
from app.models.animal import Animal, Cao, Gato, carregar_animais
from app.models.erros import ConflitoError

falhas = 0
RAIZ = pathlib.Path(__file__).parent / 'app'


def checar(ok, descricao):
    global falhas
    if ok:
        print(f'  ok      {descricao}')
    else:
        print(f'  FALHOU  {descricao}')
        falhas += 1


def recusa(funcao, erro=ValueError):
    try:
        funcao()
    except erro:
        return True
    return False


def arvores(pasta):
    return [ast.parse(p.read_text(encoding='utf-8')) for p in (RAIZ / pasta).glob('*.py')]


def codigo_de(modulo):
    return open(modulo.__file__, encoding='utf-8').read()


print('\n1. Encapsulamento: o objeto nasce valido')
checar(recusa(lambda: Cao(99, '   ', 3, 'pequeno')), 'construtor recusa nome vazio')
checar(recusa(lambda: Cao(99, 'Rex', -1, 'pequeno')), 'construtor recusa idade negativa')
checar(recusa(lambda: Cao(99, 'Rex', 31, 'pequeno')), 'construtor recusa idade acima de 30')
checar(recusa(lambda: Gato(99, 'Tom', 2, 'gigante')), 'construtor recusa porte invalido')
checar(not hasattr(Animal, 'alterar_id'), 'nao existe alterar_id')

print('\n2. Encapsulamento: Adotante valida a idade')
checar(recusa(lambda: Adotante(99, 'Teste', 17, False)), 'construtor recusa menor de 18 anos')
checar(recusa(lambda: Adotante(99, ' ', 30, False)), 'construtor recusa nome vazio')

print('\n3. Heranca: a hierarquia esta correta')
checar(issubclass(Cao, Animal), 'Cao herda de Animal')
checar(issubclass(Gato, Animal), 'Gato herda de Animal')
checar('mostrar_nome' not in Cao.__dict__, 'Cao NAO reescreve mostrar_nome: herda')

print('\n4. Heranca: cada filha escreve so a diferenca')
checar('descricao' in Cao.__dict__ and 'descricao' in Gato.__dict__,
       'Cao e Gato sobrescrevem descricao')
checar(Cao.TAXA_ADOCAO != Gato.TAXA_ADOCAO, 'a constante de classe muda de filha para filha')
rex = Cao(98, 'Rex', 3, 'pequeno')
checar(rex.descricao().startswith(Animal.descricao(rex)),
       'descricao() da filha estende a da base com super()')

print('\n5. Polimorfismo: a mesma chamada, respostas diferentes')
animais = carregar_animais()
checar(len(animais) >= 5, 'o mock tem pelo menos 5 animais')
checar({type(a).__name__ for a in animais} == {'Cao', 'Gato'},
       'o mock virou duas classes diferentes')
thor, mel, luna = animais[0], animais[1], animais[2]
checar(thor.mostrar_taxa() == 80.0 and luna.mostrar_taxa() == 50.0,
       'cada especie responde a sua taxa')
checar('passeios' in thor.descricao() and 'apartamento' in luna.descricao(),
       'cada especie responde a sua descricao')

print('\n6. Associacao: a adocao guarda objetos, nao ids')
adocoes = carregar_adocoes()
primeira = adocoes[0]
checar(isinstance(primeira.mostrar_animal(), Animal), 'mostrar_animal devolve um Animal')
checar(isinstance(primeira.mostrar_adotante(), Adotante), 'mostrar_adotante devolve um Adotante')
checar(primeira.mostrar_animal().mostrar_nome() == 'Mel', 'o encadeamento chega ao nome do animal')
checar(not primeira.mostrar_animal().esta_disponivel(), 'a adocao do mock marcou o animal como adotado')

print('\n7. Regras que dependem da associacao')
animais = carregar_animais()
adotantes = carregar_adotantes()
carregar_adocoes(animais, adotantes)
thor, luna, mingau, bolt = animais[0], animais[2], animais[3], animais[4]
ana, bruno = adotantes[0], adotantes[1]
checar(recusa(lambda: Adocao(50, thor, bruno, '2026-10-01')),
       'cao grande sem quintal e recusado')
Adocao(51, luna, bruno, '2026-10-01')
checar(recusa(lambda: Adocao(52, luna, ana, '2026-10-01'), ConflitoError),
       'animal ja adotado e conflito')
Adocao(53, mingau, ana, '2026-10-01')
checar(recusa(lambda: Adocao(54, bolt, ana, '2026-10-01'), ConflitoError),
       'adotante acima do limite e conflito')
checar(recusa(lambda: Adocao(55, bolt, adotantes[2], '  ')), 'data vazia e recusada')

print('\n8. A conta mora no objeto')
checar(primeira.valor_taxa() == 80.0, 'taxa calculada pela propria adocao')
checar(primeira.e_do_adotante(1) and not primeira.e_do_adotante(2),
       'a adocao sabe de quem e')

print('\n9. Colecoes: filtrar')
from app.controllers.adocao_controller import AdocaoController
from app.controllers.animal_controller import AnimalController
ac = AnimalController()
checar(len(ac.listar_por_especie('gato')) == 5, 'cinco gatos no mock')
checar(ac.listar_por_especie('xyz') == [], 'especie inexistente devolve lista vazia')
checar(ac.buscar(999) is None, 'animal inexistente devolve None')
adc = AdocaoController(ac.mostrar_modelos())
checar(len(ac.listar_disponiveis()) == 5, 'os animais ja adotados ficam de fora dos disponiveis')
checar(adc.listar_por_adotante(999) is None, 'adotante inexistente devolve None')
checar(adc.registrar(999, 1) is None, 'adocao de animal inexistente devolve None')

print('\n10. Camadas: a model nao conhece o FastAPI')
import app.models.adocao as ma
import app.models.adotante as mt
import app.models.animal as mn
for modulo in (ma, mt, mn):
    checar('fastapi' not in codigo_de(modulo),
           f'{modulo.__name__.split(".")[-1]}.py nao importa fastapi')

print('\n11. Camadas: o controller nao devolve codigo HTTP')
import app.controllers.adocao_controller as cad
import app.controllers.animal_controller as can
for modulo in (cad, can):
    checar('HTTPException' not in codigo_de(modulo),
           f'{modulo.__name__.split(".")[-1]}.py nao usa HTTPException')

print('\n12. Projeto: nenhum if de tipo, mocks puros, 4 regras com raise')
todos = [ast.parse(p.read_text(encoding='utf-8')) for p in RAIZ.rglob('*.py')]
testes_if = [ast.dump(n.test) for a in todos for n in ast.walk(a)
             if isinstance(n, (ast.If, ast.IfExp))]
checar(not any(t in texto for texto in testes_if
               for t in ('__class__', '__name__', "'type'", "'isinstance'")),
       'nenhum if comparando tipo ou nome de classe')
checar(not any(isinstance(n, (ast.Import, ast.ImportFrom, ast.ClassDef))
               for a in arvores('data') for n in ast.walk(a)),
       'os mocks nao tem import nem classe')
checar(sum(isinstance(n, ast.Raise) for a in arvores('models') for n in ast.walk(a)) >= 4,
       'pelo menos 4 regras com raise nas models')
checar(any(isinstance(n, ast.ListComp) and n.generators[0].ifs
           for a in arvores('controllers') for n in ast.walk(a)),
       'pelo menos um filtro com compreensao de lista')

print()
if falhas == 0:
    print('TUDO CERTO. Agora suba a API e teste no /docs.')
else:
    print(f'{falhas} verificacao(oes) falharam.')
raise SystemExit(1 if falhas else 0)
