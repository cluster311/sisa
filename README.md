# SISA
Conexión a las APIs de SISA (Sistema Integrado de Información Sanitario Argentino).  
Más info de las APIs de SISA: https://sisa.msal.gov.ar/sisadoc/docs/0203/ws_sisa.jsp  

## Padrón Unico Consolidado Operativo (PUCO)
Más info: https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp  

### Uso

Instalación

```
pip install sisa
```

Ejemplo

```python
from sisa.apis.puco import Puco
from sisa.apis import settings
settings.USER_SISA = 'xxxxxx'
settings.PASS_SISA = 'xxxxxxxxxx'

puco = Puco(dni='26453653')
resp = puco.get_info_ciudadano()
if resp['ok']:
    if resp['persona_encontrada']:
        print('Encontrado: {}. Obra social {} (RNOS:{})'.format(resp['nombre_persona'],
                                                                resp['nombre_obra_social'],
                                                                resp['id_obra_social']))


print('------------------')
print('Respuesta completa')
print(resp)
print('------------------')
```
Resultado:

```
Encontrado: VAZQUEZ FLEXES ANDRES. Obra social O.S.P. CORDOBA (APROSS) (RNOS:904001)

------------------
Respuesta completa

{
    'ok': True, 
    'persona_encontrada': True, 
    'nombre_obra_social': 'O.S.P. CORDOBA (APROSS)', 
    'nombre_persona': 'VAZQUEZ FLEXES ANDRES', 
    'id_obra_social': '904001', 
    'tipo_doc': 'DNI',

# otros detalles
    'raw': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><pucoResponse><resultado>OK</resultado><puco><coberturaSocial>O.S.P. CORDOBA (APROSS)</coberturaSocial><denominacion>VAZQUEZ FLEXES ANDRES</denominacion><nrodoc>26453653</nrodoc><rnos>904001</rnos><tipodoc>DNI</tipodoc></puco></pucoResponse>', 
    'all_fields': {
        'resultado': 'OK', 
        'puco': None, 
        'puco__coberturaSocial': 'O.S.P. CORDOBA (APROSS)', 
        'puco__denominacion': 'VAZQUEZ FLEXES ANDRES', 
        'puco__nrodoc': '26453653', 
        'puco__rnos': '904001', 
        'puco__tipodoc': 'DNI'}, 
}
------------------
```