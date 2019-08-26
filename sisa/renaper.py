"""
Padrón Unico Consolidado Operativo (PUCO)
https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_ws_131.jsp
"""
from sisa import settings
import requests
import xml.etree.ElementTree as ET
from oss_ar.oss import ObraSocialArgentina
import json
import logging
logger = logging.getLogger(__name__)


class Renaper:
    """
    Obtener información de RENAPER del ciudadano argentino
    """
    
    SERVICE_URL = 'https://sisa.msal.gov.ar/sisa/services/rest/cmdb/obtener/'

    # campos de respuesta 
    dni = None
    codigo_sisa_renaper = None  # codigo de SISA si esta en renaper (?) si no es cero
    codigo_sisa = None
    codigo_renaper = None
    padron_sisa = None  # SI | NO
    tipo_doc = None  # tipo de documento, en general "DNI"
    nombre = None
    apellido = None
    sexo = None
    fecha_nacimiento = None
    cobertura_social = None  # algo como O.S.P. CORDOBA (APROSS)
    rnos = None  # código único de la obra social
    oss = None  # datos de la obra social de librería externa
    provincia = None
    departamento = None
    localidad = None
    domicilio = None
    estado_civil = None
    tipo_cobertura_vigente = None
    piso_depto = None
    codigo_postal = None
    pais_nacimiento = None
    provincia_nacimiento = None
    localidad_nacimiento = None
    nacionalidad = None
    fallecido = None
    fecha_fallecido = None
    donante = None
    coberturas = []  # coberturas de salud
    codigo_bahra_provincia = None
    codigo_bahra_departamento = None
    codigo_bahra_localidad = None
    
    # mis extras
    extra_fields = {}  # campos nuevos que podrían venir en el futuro
    raw_response = None
    status_response = None
    last_error = None

    def __init__(self, dni, codigo_sisa=None, sexo=None):
        self.dni = dni
        self.codigo_sisa = codigo_sisa
        self.sexo = sexo
    
    def __str__(self):
        return f'{self.nombre} {self.apellido} DNI: {self.dni}.'

    def get_info_ciudadano(self):
        """ Ejemplo de resultado
            <Ciudadano>
                <resultado>OK</resultado>
                <id>3381518</id>
                <codigoSISA>4400000533</codigoSISA>
                <identificadoRenaper>24432867</identificadoRenaper>
                <PadronSISA>SI</PadronSISA>
                <tipoDocumento>DNI</tipoDocumento>
                <nroDocumento>34521364</nroDocumento>
                <apellido>MONTI LORUSSO</apellido>
                <nombre>BRUNO ADRIAN</nombre>
                <sexo>M</sexo>
                <fechaNacimiento>24-06-1989 00:01</fechaNacimiento>
                <estadoCivil>Casado/a</estadoCivil>
                <tipoCoberturaVigente>Obra social</tipoCoberturaVigente>
                <obraSocialVigente>OBRA SOCIAL DE LA UNION OBRERA METALURGICA DE LA REPUBLICA ARGENTINA</obraSocialVigente>
                <rnos>112103</rnos>
                <provincia>Buenos Aires</provincia>
                <departamento>Lomas de Zamora</departamento>
                <localidad>Temperley</localidad>
                <domicilio>ORURO 640</domicilio>
                <pisoDpto />
                <codigoPostal>1834</codigoPostal>
                <paisNacimiento>Argentina</paisNacimiento>
                <provinciaNacimiento>Buenos Aires</provinciaNacimiento>
                <localidadNacimiento />
                <nacionalidad>Argentina</nacionalidad>
                <fallecido>NO</fallecido>
                <fechaFallecido />
                <donante>NULL</donante>
            </Ciudadano>
        """
        logger.info(f'Getting PUCO info ciudadano {self.dni}')
        respuesta = {}

        url = self.SERVICE_URL.format(dni=self.dni)
        params = {'usuario': settings.USER_SISA,
                  'clave': settings.PASS_SISA,
                  'nrodoc': self.dni,
                  }
        if self.codigo_sisa is not None:
            # Dato numérico que identifica de forma única a cada persona en el SISA.
            params['codigo'] = self.codigo_sisa
        if self.sexo is not None:
            params['sexo'] = self.sexo  # F o M
                      
        # NO FUNCIOAN SIN ESOS HEADERS (aunque el resultado es XML)
        headers = {"Content-Type": "application/json; charset=utf-8"}  

        try:
            response = requests.get(url,
                                    params=params,
                                    headers=headers,
                                    timeout=30)
        except Exception as e:
            self.raw_response = response.content
            self.status_response = response.status_code
            self.last_error = f'Error POST RENAPER: {e}'
            logger.error('{} status:{}'.fomrat(self.last_error, self.status_response))
            respuesta['ok'] = False
            return respuesta
        
        self.status_response = response.status_code
        self.raw_response = response.content
        logger.info('respuesta de RENAPER: {} {}'.format(response.status_code, response.content))

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
                    self.last_error = f'Error de autentificacion, revise sus credenciales'
                    logger.error(self.last_error)
                elif valor == 'ERROR_INESPERADO':
                    respuesta['ok'] = False
                    self.last_error = 'La llamada no es correcta o hay otro problema.'
                    logger.error(self.last_error)
                elif valor == 'NO_TIENE_QUOTA_DISPONIBLE':
                    respuesta['ok'] = False
                    self.last_error = 'El usuario no tiene cuota de uso asignada.'
                    logger.error(self.last_error)
                elif valor == 'ERROR_DATOS':
                    respuesta['ok'] = False
                    self.last_error = 'La llamada no es correcta.'
                    logger.error(self.last_error)
                elif valor == 'SERVICIO_RENAPER_NO_DISPONIBLE':
                    respuesta['ok'] = False
                    self.last_error = 'El Servicio RENAPER no se encuentra disponible.'
                    logger.error(self.last_error)
                elif valor == 'MULTIPLE_RESULTADO':
                    respuesta['ok'] = False
                    self.last_error = 'Se ha encontrado más de un resultado. Se sugiere incluir el parámetro Sexo en la consulta.'
                    logger.error(self.last_error)
                else:
                    respuesta['ok'] = False
                    self.last_error = f'Respuesta no reconocida: {valor}'
                    logger.error(self.last_error)
            
            elif campo == 'id':
                # id en sisa. 0 => esta en renaper pero no en SISA
                self.codigo_sisa_renaper = valor  # nombre de la oss # ej: O.S.P. CORDOBA (APROSS)
            elif campo == 'codigoSISA':  # nombre + apellido de la persona
                self.codigo_sisa = valor
            elif campo == 'nroDocumento':  # nro a secas del DNI
                self.dni = valor
            elif campo == 'identificadoRenaper':
                self.codigo_renaper = valor
            elif campo == 'PadronSISA':
                self.padron_sisa = valor
            elif campo == 'tipoDocumento':
                self.tipo_doc = valor
            elif campo == 'apellido':
                self.apellido = valor
            elif campo == 'nombre':
                self.nombre = valor
            elif campo == 'sexo':
                self.sexo = valor
            elif campo == 'fechaNacimiento':
                self.fecha_nacimiento = valor
            elif campo == 'estadoCivil':
                self.estado_civil = valor  # ej Casado/a
            elif campo == 'tipoCoberturaVigente':
                self.tipo_cobertura_vigente = valor  # ej: Obra social
            elif campo == 'obraSocialVigente': 
                self.cobertura_social = valor   # ej OBRA SOCIAL DE LA UNION OBRERA METALURGICA
            elif campo == 'rnos':  # nombre + apellido de la persona
                self.rnos = valor
            elif campo == 'provincia':  # nombre + apellido de la persona
                self.provincia = valor
            elif campo == 'departamento':  # nombre + apellido de la persona
                self.departamento = valor
            elif campo == 'localidad':  # nombre + apellido de la persona
                self.localidad = valor
            elif campo == 'domicilio':  # nombre + apellido de la persona
                self.domicilio = valor
            elif campo == 'pisoDpto':  # nombre + apellido de la persona
                self.piso_depto = valor
            elif campo == 'codigoPostal':  # nombre + apellido de la persona
                self.codigo_postal = valor
            elif campo == 'paisNacimiento':  # nombre + apellido de la persona
                self.pais_nacimiento = valor
            elif campo == 'provinciaNacimiento':  # nombre + apellido de la persona
                self.provincia_nacimiento = valor
            elif campo == 'localidadNacimiento':  # nombre + apellido de la persona
                self.localidad_nacimiento = valor
            elif campo == 'nacionalidad':  # nombre + apellido de la persona
                self.nacionalidad = valor
            elif campo == 'fallecido':  # nombre + apellido de la persona
                self.fallecido = valor  # Ej NO
            elif campo == 'fechaFallecido':  # nombre + apellido de la persona
                self.fecha_fallecido = valor
            elif campo == 'donante':  # nombre + apellido de la persona
                self.donante = valor  # Ej NULL
            elif campo == 'cobertura':
                self.__procesar_cobertura(child)
            elif campo == 'codigoBahraProvincia':  # nombre + apellido de la persona
                self.codigo_bahra_provincia = valor  # Ej NULL
            elif campo == 'codigoBahraDepartamento':  # nombre + apellido de la persona
                self.codigo_bahra_departamento = valor  # Ej NULL
            elif campo == 'codigoBahraLocalidad':  # nombre + apellido de la persona
                self.codigo_bahra_localidad = valor  # Ej NULL
            else:
                self.extra_fields[campo] = valor
                logger.error(f'Campo no esperado {campo} = {valor}')

        # tomar la última cobertura
        # FIXME
        for cobertura in self.coberturas:
            self.cobertura_social = cobertura['nombreObraSocial']
            self.rnos = cobertura['rnos']
            # agregar info oficial de la obra social
            if self.rnos is not None:
                oss = ObraSocialArgentina(rnos=self.rnos)
                self.oss = oss.as_dict()

        logger.info(f'Respuesta RENAPER: {respuesta}')
        return respuesta
    
    def __procesar_cobertura(self, cobertura_xml):
        """ llego una (pueden ser varias con diferente fecha) cobertura encapsulada
        Ej: <cobertura>
                <fechaActualizacion>27-09-2018 20:02</fechaActualizacion>
                <nombreObraSocial>O.S.P. CORDOBA (APROSS)</nombreObraSocial>
                <origen>PUCO</origen>
                <rnos>904001</rnos>
                <tipoCobertura>Obra social</tipoCobertura>
                <vigenciaDesde>\'\'sin dato\'\'</vigenciaDesde>
            </cobertura>
        """
        cobertura = {}
        for detalle in cobertura_xml:
            campo = detalle.tag.strip()
            valor = None if detalle.text is None else detalle.text.strip()
            cobertura[campo] = valor

        self.coberturas.append(cobertura)
