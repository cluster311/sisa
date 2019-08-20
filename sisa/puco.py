"""
Padrón Unico Consolidado Operativo (PUCO)
https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp
"""
from sisa.settings import (URL_API_REST_PUCO,
                      USER_SISA,
                      PASS_SISA,
                      VERIFY_SSL_SISA
                      )
import requests
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger(__name__)


class PUCO():
    """
    Obtener información de la Obra Social registrada de un ciudadano argentino
    """

    def __init__(self, dni):
        self.dni = dni

    def get_info_ciudadano(self):
        """ obtener la cobertura de un ciudadano argentino
            Ejemplo de resultado

            <puco>
            <resultado>OK</resultado>
                <coberturaSocial>O.S.P. CIUDAD AUT. DE BUENOS AIRES (ObSBA)</coberturaSocial>
                <denominacion>AGOSTINO RODRIGO LEONARDO</denominacion>
                <nrodoc>44003375</nrodoc>
                <tipodoc>DNI</tipodoc>
                <rnos>901001</rnos>
            </puco>
        """
        logger.info(f'Getting PUCO info ciudadano {self.dni}')
        respuesta = {}

        url = settings.URL_API_PUCO.format(self.dni)
        data = {"usuario": USER_ISA, "clave": PASS_SISA}
        data_str = json.dumps(data)
        
        # NO FUNCIOAN SIN ESOS HEADERS (aunque el resultado es XML)
        headers = {"Content-Type": "application/json; charset=utf-8"}  

        try:
            response = requests.post(url, data=data_str, headers=headers, verify=VERIFY_SSL_SISA)
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

        respuesta['raw'] = {}
        for child in xmldata:

            campo = child.tag.strip()
            valor = child.text.strip()
            # por las dudas grabo todo
            respuesta['raw'][campo] = valor

            if campo == 'resultado':
                if valor == 'OK':  # REGISTRO_NO_ENCONTRADO
                    respuesta['ok'] = True
                    respuesta['persona_encontrada'] = True
                elif valor == 'REGISTRO_NO_ENCONTRADO':
                    # la persona no esta en la base de PUCO
                    respuesta['ok'] = True
                    respuesta['persona_encontrada'] = False
                else:
                    respuesta['ok'] = False
                    respuesta['error'] = f'Respuesta no reconocida: {valor}'
                    logger.error(f'Respuesta PUCO no reconocida {valor}')
            elif campo == 'coberturaSocial':
                respuesta['nombre_obra_social'] = valor  # nombre de la oss # ej: O.S.P. CORDOBA (APROSS)
            elif campo == 'denominacion':  # nombre + apellido de la persona
                respuesta['nombre_persona'] = valor
            elif campo == 'nrodoc':  # nro a secas del DNI
                pass  # es el mismo que le pase como parámetro
            elif campo == 'rnos':  # ID de la obra social. Ej 904001
                respuesta['id_obra_social'] = valor
            elif campo == 'tipodoc':  # ex DNI
                respuesta['tipo_doc'] = valor

        logger.info(f'Respuesta PUCO: {respuesta}')
        return respuesta