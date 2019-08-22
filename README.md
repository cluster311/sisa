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

#### Credenciales requeridas
Definir las variables de entorno _USER_SISA_ y _PASS_SISA_ con los valores recibidos por SISA. 

```
export USER_SISA='my-sisa-user'
export PASS_SISA='my-sisa-pass'
```

#### Ejemplo en python

```python

from sisa.puco import Puco

puco = Puco(dni='26453653')
resp = puco.get_info_ciudadano()
if resp['ok']:
    if resp['persona_encontrada']:
        print(f'''Encontrado: {puco.dni} ({puco.tipo_doc}) {puco.denominacion}
                [{puco.rnos}] {puco.cobertura_social}''')
        
    else:
        print(f'Persona no encontrada: {puco.last_error}')
else:
    print(f'Error: {puco.last_error}')


print('------------------')
print('Respuesta completa')
print(f'Status: {puco.status_response}')
print(puco.raw_response)
print('------------------')
```

#### Resultado

```
Encontrado: 26453653 (DNI) VAZQUEZ FLEXES ANDRES
                [904001] O.S.P. CORDOBA (APROSS)
------------------
Respuesta completa
Status: 200
b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><pucoResponse><resultado>OK</resultado><puco><coberturaSocial>O.S.P. CORDOBA (APROSS)</coberturaSocial><denominacion>VAZQUEZ FLEXES ANDRES</denominacion><nrodoc>26453653</nrodoc><rnos>904001</rnos><tipodoc>DNI</tipodoc></puco></pucoResponse>'
------------------
```

#### Ejemplo en consola

```
sisa_puco --dni 25411233

{'dni': '25411233', 'status_response': 200, 'raw_response': b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><pucoResponse><resultado>OK</resultado><puco><coberturaSocial>OBRA SOCIAL DEL PERSONAL ASOCIADO A ASOCIACION MUTUAL SANCOR</coberturaSocial><denominacion>PASTRANA GABRIEL FEDERICO</denominacion><nrodoc>25411233</nrodoc><rnos>3009</rnos><tipodoc>DNI</tipodoc></puco></pucoResponse>', 'cobertura_social': 'OBRA SOCIAL DEL PERSONAL ASOCIADO A ASOCIACION MUTUAL SANCOR', 'denominacion': 'PEREZ JUAN CARLOS', 'rnos': '3009', 'tipo_doc': 'DNI'}
```