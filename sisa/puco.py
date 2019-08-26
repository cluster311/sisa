"""
Padrón Unico Consolidado Operativo (PUCO)
https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp
"""
from sisa import settings
import requests
import xml.etree.ElementTree as ET
import json
from oss_ar.oss import ObraSocialArgentina
import logging
logger = logging.getLogger(__name__)


class Puco:
    """
    Obtener información de la Obra Social registrada de un ciudadano argentino
    """
    SERVICE_URL = 'https://sisa.msal.gov.ar/sisa/services/rest/puco/{dni}'

    # campos de respuesta 
    dni = None
    cobertura_social = None  # algo como O.S.P. CORDOBA (APROSS)
    denominacion = None  # Nombre completo de la persona
    rnos = None  # código único de la obra social
    oss = None  # datos de la obra social de librería externa
    tipo_doc = None  # tipo de documento, en general "DNI"
    
    # mis extras
    extra_fields = {}  # campos nuevos que podrían venir en el futuro
    raw_response = None
    status_response = None
    last_error = None

    def __init__(self, dni):
        self.dni = dni
    
    def __str__(self):
        return f'{self.denominacion} DNI: {self.dni}. Obra social: [{self.rnos}] {self.cobertura_social}'

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

        url = self.SERVICE_URL.format(dni=self.dni)
        params = {"usuario": settings.USER_SISA, "clave": settings.PASS_SISA}
        data_str = json.dumps(params)
        
        # NO FUNCIOAN SIN ESOS HEADERS (aunque el resultado es XML)
        headers = {"Content-Type": "application/json; charset=utf-8"}  

        try:
            response = requests.post(url, data=data_str, headers=headers)
        except Exception as e:
            self.raw_response = response.content
            self.status_response = response.status_code
            self.last_error = f'Error POST PUCO: {e}'
            logger.error('{} status:{}'.fomrat(self.last_error, self.status_response))
            respuesta['ok'] = False
            return respuesta
        
        self.status_response = response.status_code
        self.raw_response = response.content
        logger.info('respuesta de PUCO: {} {}'.format(response.status_code, response.content))

        encode_to = 'utf-8'
        data = response.content.decode(encode_to)
        xmldata = ET.fromstring(data)

        for child in xmldata:

            campo = child.tag.strip()
            valor = None if child.text is None else child.text.strip()
            
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
                    self.last_error = 'Error de autentificacion, revise sus credenciales'
                    logger.error(self.last_error)
                elif valor == 'ERROR_INESPERADO':
                    respuesta['ok'] = False
                    self.last_error = 'La llamada no es correcta o hay otro problema.'
                    logger.error(self.last_error)
                elif valor == 'NO_TIENE_QUOTA_DISPONIBLE':
                    respuesta['ok'] = False
                    self.last_error = 'No tiene cuota de uso asignada'
                    logger.error(self.last_error)
                elif valor == 'ERROR_DATOS':
                    respuesta['ok'] = False
                    self.last_error = 'La llamada no es correcta o hay otro problema.'
                    logger.error(self.last_error)
                elif valor == 'MULTIPLE_RESULTADO':
                    respuesta['ok'] = False
                    self.last_error = 'Se ha encontrado más de un resultado.'
                    logger.error(self.last_error)
                elif valor == 'LIMITE_EXCEDIDO':
                    respuesta['ok'] = False
                    self.last_error = 'Se ha excedido la cantidad de resultados.'
                    logger.error(self.last_error)
                else:
                    respuesta['ok'] = False
                    self.last_error = f'Respuesta no reconocida: {valor}'
                    logger.error(self.last_error)
            elif campo == 'puco':  # ingresar a los detalles
                for detalle in child:
                    campo_detalle = detalle.tag.strip()
                    valor = None if detalle.text is None else detalle.text.strip()
                    
                    if campo_detalle == 'coberturaSocial':
                        self.cobertura_social = valor  # nombre de la oss # ej: O.S.P. CORDOBA (APROSS)
                    elif campo_detalle == 'denominacion':  # nombre + apellido de la persona
                        self.denominacion = valor
                    elif campo_detalle == 'nrodoc':  # nro a secas del DNI
                        pass  # es el mismo que le pase como parámetro
                    elif campo_detalle == 'rnos':  # ID de la obra social. Ej 904001
                        self.rnos = valor
                    elif campo_detalle == 'tipodoc':  # ex DNI
                        self.tipo_doc = valor
                    else:
                        if 'puco' not in self.extra_fields:
                            self.extra_fields['puco'] = {}
                        self.extra_fields['puco'][campo_detalle] = valor
            else:
                self.extra_fields[campo] = valor

        logger.info(f'Respuesta PUCO: {respuesta}')

        # agregar info oficial de la obra social
        if self.rnos is not None:
            oss = ObraSocialArgentina(rnos=self.rnos)
            self.oss = oss.as_dict()

        return respuesta