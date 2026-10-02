from fastapi.testclient import TestClient
from main import app

c = TestClient(app)
falhas = 0

def t(desc, resp, esperado, verif=None):
    global falhas
    ok = resp.status_code == esperado
    extra = ''
    if ok and verif:
        try:
            ok = verif(resp.json())
        except Exception as e:
            ok = False; extra = f' ({e})'
    print(('  ok      ' if ok else '  FALHOU  ') + f'{desc} -> {resp.status_code}{extra}')
    if not ok: falhas += 1

print('\nPRODUTOS')
t('GET  /api/produtos', c.get('/api/produtos'), 200, lambda j: len(j) == 6)
t('GET  /api/produtos/1', c.get('/api/produtos/1'), 200, lambda j: j['nome'].startswith('Arroz'))
t('GET  /api/produtos/99', c.get('/api/produtos/99'), 404)
t('GET  /api/produtos/categoria/graos', c.get('/api/produtos/categoria/Grãos'), 200, lambda j: len(j) == 3)
t('GET  /api/produtos/categoria/xyz', c.get('/api/produtos/categoria/xyz'), 404)

print('\nLOGIN')
t('POST /api/login bia ok', c.post('/api/login', json={'nome':'bia','senha':'bia123'}), 200,
  lambda j: j['perfil'] == 'visitante' and j['permissoes'] == ['ver_ofertas'])
t('POST /api/login caio ok', c.post('/api/login', json={'nome':'caio','senha':'caio123'}), 200,
  lambda j: j['perfil'] == 'moderador' and len(j['permissoes']) == 4)
t('POST /api/login senha errada', c.post('/api/login', json={'nome':'ana','senha':'x'}), 401)
t('POST /api/login sem campo', c.post('/api/login', json={'nome':'ana'}), 422)
t('POST /api/login nao vaza senha', c.post('/api/login', json={'nome':'ana','senha':'ana123'}), 200,
  lambda j: 'senha' not in j)

print('\nMERCADOS')
t('GET  /api/mercados', c.get('/api/mercados'), 200, lambda j: len(j) == 3)
t('GET  /api/mercados/1', c.get('/api/mercados/1'), 200, lambda j: j['nome'] == 'Mercado Silva')
t('GET  /api/mercados/99', c.get('/api/mercados/99'), 404)
t('GET  /api/mercados/1/ofertas', c.get('/api/mercados/1/ofertas'), 200, lambda j: len(j) == 3)
t('GET  /api/mercados/99/ofertas', c.get('/api/mercados/99/ofertas'), 404)

print('\nOFERTAS E COMPARATIVO')
t('GET  /api/ofertas', c.get('/api/ofertas'), 200, lambda j: len(j) == 7)
t('GET  /api/ofertas/1', c.get('/api/ofertas/1'), 200, lambda j: j['preco'] == 19.9)
t('GET  /api/ofertas/99', c.get('/api/ofertas/99'), 404)
t('GET  /api/produtos/1/ofertas', c.get('/api/produtos/1/ofertas'), 200,
  lambda j: [o['preco'] for o in j] == [19.9, 21.0, 22.5])
t('GET  /api/produtos/6/ofertas', c.get('/api/produtos/6/ofertas'), 404)
t('GET  /api/produtos/1/comparativo', c.get('/api/produtos/1/comparativo'), 200,
  lambda j: j['menor_preco'] == 19.9 and j['economia'] == 5.0 and j['mercados'] == 3)
t('GET  /api/produtos/6/comparativo', c.get('/api/produtos/6/comparativo'), 404)

print('\nRAIZ E DOCS')
t('GET  /', c.get('/'), 200)
t('GET  /docs', c.get('/docs'), 200)
t('GET  /openapi.json', c.get('/openapi.json'), 200)

print()
print('TODAS AS ROTAS OK' if falhas == 0 else f'{falhas} falha(s)')
