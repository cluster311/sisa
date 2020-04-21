# SISA
Conexión a las APIs de SISA (Sistema Integrado de Información Sanitario Argentino).  
Más info de las APIs de SISA: https://sisa.msal.gov.ar/sisadoc/docs/0203/ws_sisa.jsp  

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

## Obras sociales

Si la obra social existe entonces se devuelven datos adicionales de ella a través de la librería [oss-ar](https://pypi.org/project/oss-ar/).  


## APIs

### Padrón Unico Consolidado Operativo (PUCO)
Más info: https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp  

#### Ejemplo en python

```python

from sisa.puco import Puco

puco = Puco(dni='26453653')
resp = puco.get_info_ciudadano()
if resp['ok']:
    if resp['persona_encontrada']:
        print(f'''Encontrado: {puco.dni} ({puco.tipo_doc}) {puco.denominacion}
                [{puco.rnos}] {puco.cobertura_social}
                OSS: {puco.oss}''')
        
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
                OSS: {'rnos': '904001', 'exists': True, 'nombre': 'O.S.P. CORDOBA (APROSS)', 'tipo_de_cobertura': 'Obra social', 'sigla': 'APROSS', 'provincia': 'Córdoba', 'localidad': '', 'domicilio': 'Sin especificar', 'cp': '', 'telefonos': [], 'emails': [], 'web': None}

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

### Re.Na.Per
Registro Nacional de las Personas (Argetina).  
https://sisa.msal.gov.ar/sisadoc/docs/050202/cmdb_ws_042.jsp  

#### Ejemplo en python

```python

from sisa.renaper import Renaper

rena = Renaper(dni='26453653')
resp = rena.get_info_ciudadano()
if resp['ok']:
    if resp['persona_encontrada']:
        print(f'''Encontrado: {rena.dni} ({rena.tipo_doc}) {rena.nombre} {rena.apellido}
                [{rena.rnos}] {rena.cobertura_social}
                OSS: {rena.oss}''')
        
    else:
        print(f'Persona no encontrada: {rena.last_error}')
else:
    print(f'Error: {rena.last_error}')


print('------------------')
print('Respuesta completa')
print(f'Status: {rena.status_response}')
print(rena.raw_response)
print('------------------')

```

#### Resultado

```
Encontrado: 26153653 (DNI) JUAN PEREZ
                [904001] O.S.P. CORDOBA (APROSS)
                OSS: {'rnos': '904001', 'exists': True, 'nombre': 'O.S.P. CORDOBA (APROSS)', 'tipo_de_cobertura': 'Obra social', 'sigla': 'APROSS', 'provincia': 'Córdoba', 'localidad': '', 'domicilio': 'Sin especificar', 'cp': '', 'telefonos': [], 'emails': [], 'web': None}

------------------
Respuesta completa
Status: 200
b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Ciudadano><resultado>OK</resultado><id>7051139662</id><codigoSISA>1220919305</codigoSISA><identificadoRenaper>37006105</identificadoRenaper><PadronSISA>SI</PadronSISA><tipoDocumento>DNI</tipoDocumento><nroDocumento>26153653</nroDocumento><apellido>PEREZ</apellido><nombre>JUAN</nombre><sexo>M</sexo><fechaNacimiento>07-06-1978 00:00</fechaNacimiento><estadoCivil> </estadoCivil><cobertura><fechaActualizacion>30-09-2018 20:17</fechaActualizacion><nombreObraSocial>O.S.P. CORDOBA (APROSS)</nombreObraSocial><origen>PUCO</origen><rnos>904001</rnos><tipoCobertura>Obra social</tipoCobertura><vigenciaDesde>\'\'sin dato\'\'</vigenciaDesde></cobertura><codigoBahraProvincia>14</codigoBahraProvincia><provincia>C\xc3\xb3rdoba</provincia><codigoBahraDepartamento>21</codigoBahraDepartamento><departamento>Col\xc3\xb3n</departamento><codigoBahraLocalidad>200</codigoBahraLocalidad><localidad>MENDIOLAZA</localidad><domicilio>CUATRO 16</domicilio><pisoDpto> </pisoDpto><codigoPostal>5107</codigoPostal><paisNacimiento>Argentina</paisNacimiento><provinciaNacimiento> </provinciaNacimiento><localidadNacimiento> </localidadNacimiento><nacionalidad> </nacionalidad><fallecido>NO</fallecido><fechaFallecido> </fechaFallecido><donante>NULL</donante></Ciudadano>'

```

## Tests

```
python -m pytest
```