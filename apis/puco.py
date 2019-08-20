"""
Padrón Unico Consolidado Operativo (PUCO)
https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp
"""
from sisa.apis import settings
import requests
import xml.etree.ElementTree as ET
import json
import logging
logger = logging.getLogger(__name__)


class Puco():
    """
    Obtener información de la Obra Social registrada de un ciudadano argentino
    """

    def __init__(self, dni):
        self.dni = dni

    def get_info_ciudadano(self):
        """ obtener la cobertura de un ciudadano argentino
            Ejemplo de resultado
            <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <pucoResponse>
                <resultado>OK</resultado>
                <puco>
                    <coberturaSocial>O.S.P. CORDOBA (APROSS)</coberturaSocial>
                    <denominacion>VAZQUEZ FLEXES ANDRES</denominacion>
                    <nrodoc>26453653</nrodoc>
                    <rnos>904001</rnos>
                    <tipodoc>DNI</tipodoc>
                </puco>
            </pucoResponse>
        """
        logger.info(f'Getting PUCO info ciudadano {self.dni}')
        respuesta = {}

        url = settings.URL_API_REST_PUCO.format(dni=self.dni)
        params = {"usuario": settings.USER_SISA, "clave": settings.PASS_SISA}
        data_str = json.dumps(params)
        
        # NO FUNCIOAN SIN ESOS HEADERS (aunque el resultado es XML)
        headers = {"Content-Type": "application/json; charset=utf-8"}  

        try:
            response = requests.post(url, data=data_str, headers=headers, verify=settings.VERIFY_SSL_SISA)
        except Exception as e:
            error = 'Error POST PUCO (status: {}) {}. Contenido {}'.format(response.status_code, e, response.content)
            logger.error(error)
            respuesta['ok'] = False
            respuesta['error'] = error
            return respuesta
        
        logger.info('respuesta de PUCO: {} {}'.format(response.status_code, response.content))

        encode_to = 'utf-8'
        data = response.content.decode(encode_to)
        xmldata = ET.fromstring(data)

        respuesta['raw'] = data
        respuesta['all_fields'] = {}
        for child in xmldata:

            campo = child.tag.strip()
            valor = None if child.text is None else child.text.strip()
            # por las dudas grabo todo
            respuesta['all_fields'][campo] = valor
            
            if campo == 'resultado':
                if valor == 'OK':  # REGISTRO_NO_ENCONTRADO
                    respuesta['ok'] = True
                    respuesta['persona_encontrada'] = True
                elif valor == 'REGISTRO_NO_ENCONTRADO':
                    # la persona no esta en la base de PUCO
                    respuesta['ok'] = True
                    respuesta['persona_encontrada'] = False
                elif valor == 'ERROR_AUTENTICACION':
                    respuesta['ok'] = False
                    respuesta['error'] = f'Error de autentificacion, revise sus credenciales: {params}'
                else:
                    respuesta['ok'] = False
                    respuesta['error'] = f'Respuesta no reconocida: {valor}'
                    logger.error(f'Respuesta PUCO no reconocida {valor}')

            if campo == 'puco':  # ingresar
                for detalle in child:
                    campo_detalle = detalle.tag.strip() 
                    valor = None if detalle.text is None else detalle.text.strip()
                    respuesta['all_fields'][f'puco__{campo_detalle}'] = valor
                    
                    if campo_detalle == 'coberturaSocial':
                        respuesta['nombre_obra_social'] = valor  # nombre de la oss # ej: O.S.P. CORDOBA (APROSS)
                    elif campo_detalle == 'denominacion':  # nombre + apellido de la persona
                        respuesta['nombre_persona'] = valor
                    elif campo_detalle == 'nrodoc':  # nro a secas del DNI
                        pass  # es el mismo que le pase como parámetro
                    elif campo_detalle == 'rnos':  # ID de la obra social. Ej 904001
                        respuesta['id_obra_social'] = valor
                    elif campo_detalle == 'tipodoc':  # ex DNI
                        respuesta['tipo_doc'] = valor

        logger.info(f'Respuesta PUCO: {respuesta}')
        return respuesta