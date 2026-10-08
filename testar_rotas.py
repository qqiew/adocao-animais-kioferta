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
            ok = False
            extra = f' ({e})'
    print(('  ok      ' if ok else '  FALHOU  ') + f'{desc} -> {resp.status_code}{extra}')
    if not ok:
        falhas += 1


def adotar(animal_id, adotante_id, **extra):
    return c.post('/api/adocoes',
                  json={'animal_id': animal_id, 'adotante_id': adotante_id, **extra})


print('\nANIMAIS')
t('GET  /api/animais', c.get('/api/animais'), 200, lambda j: len(j) == 6)
t('GET  /api/animais/1', c.get('/api/animais/1'), 200, lambda j: j['nome'] == 'Thor')
t('GET  /api/animais/999', c.get('/api/animais/999'), 404)
t('GET  /api/animais/abc', c.get('/api/animais/abc'), 422)
t('GET  /api/animais/disponiveis', c.get('/api/animais/disponiveis'), 200,
  lambda j: len(j) == 5 and all(not a['adotado'] for a in j))
t('GET  /api/animais/especie/gato', c.get('/api/animais/especie/gato'), 200,
  lambda j: len(j) == 3 and all(a['especie'] == 'gato' for a in j))
t('GET  /api/animais/especie/cao', c.get('/api/animais/especie/cao'), 200, lambda j: len(j) == 3)
t('GET  /api/animais/especie/xyz', c.get('/api/animais/especie/xyz'), 404)

print('\nADOCOES')
t('POST /api/adocoes ok', adotar(3, 2), 201,
  lambda j: j['animal'] == 'Luna' and j['adotante'] == 'Bruno Lima' and j['taxa'] == 50.0)
t('POST /api/adocoes data informada', adotar(4, 1, data='2026-10-01'), 201,
  lambda j: j['data'] == '2026-10-01')
t('POST /api/adocoes animal ja adotado', adotar(3, 4), 409)
t('POST /api/adocoes acima do limite', adotar(5, 1), 409)
t('POST /api/adocoes cao grande sem quintal', adotar(1, 2), 422)
t('POST /api/adocoes data vazia', adotar(6, 3, data='  '), 422)
t('POST /api/adocoes animal inexistente', adotar(999, 1), 404)
t('POST /api/adocoes adotante inexistente', adotar(6, 999), 404)
t('POST /api/adocoes sem campo', c.post('/api/adocoes', json={'animal_id': 6}), 422)
t('POST /api/adocoes cao grande com quintal', adotar(1, 3), 201, lambda j: j['taxa'] == 80.0)

print('\nHISTORICO E RELATORIO')
t('GET  /api/adotantes/1/adocoes', c.get('/api/adotantes/1/adocoes'), 200, lambda j: len(j) == 2)
t('GET  /api/adotantes/4/adocoes vazio', c.get('/api/adotantes/4/adocoes'), 200, lambda j: j == [])
t('GET  /api/adotantes/999/adocoes', c.get('/api/adotantes/999/adocoes'), 404)
t('GET  /api/relatorio/taxas', c.get('/api/relatorio/taxas'), 200,
  lambda j: j['adocoes'] == 4 and j['total_taxas'] == 80.0 + 50.0 + 50.0 + 80.0)

print('\nRAIZ E DOCS')
t('GET  /', c.get('/'), 200)
t('GET  /docs', c.get('/docs'), 200)
t('GET  /openapi.json', c.get('/openapi.json'), 200)

print()
print('TODAS AS ROTAS OK' if falhas == 0 else f'{falhas} falha(s)')
