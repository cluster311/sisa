# SISA
Conexión a las APIs de SISA (Sistema Integrado de Información Sanitario Argentino).  
Más info de las APIs de SISA: https://sisa.msal.gov.ar/sisadoc/docs/0203/ws_sisa.jsp  

## Padrón Unico Consolidado Operativo (PUCO)
Más info: https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp  

### Uso

```python
from sisa.puco import PUCO

puco = PUCO(dni='26453653')
resp = puco.get_info_ciudadano()
print(resp)

```