import os

# credenciales brindadas por SISA
# cargar en local_settings
USER_SISA = os.environ.get('USER_SISA', 'test')
PASS_SISA = os.environ.get('PASS_SISA', 'test')

test_data = {
    'puco': {
        'cobertura_social': ['O.S.P. CORDOBA (APROSS)', 'TEST OSS'],
        'denominacion': ['Marta Gonzalez', 'Raul Rodriguez', 'Gerardo Martinez'],
        'rnos': ['904001', '256349', '369584'],
        'tipo_doc': ['DNI']
    },
    'renaper': {
        'codigo_sisa': ['4400000533', '4400000534'],
        'codigo_renaper': ['24432867', '24432868'],
        'tipo_doc': ['DNI'],
        'apellido': ['Martinez', 'Garcia', 'Rodriguez'],
        'nombre': ['Margarita', 'Roberto', 'Fernando'],
        'sexo': ['F', 'M'],
        'fecha_nacimiento': ['26-05-1986 00:00', '12-03-1964 00:00', '23-10-1994 00:00'],
        'estado_civil': ['Casado/a', 'Soltero/a'],
        'tipo_cobertura_vigente': ['Obra Social'],
        'cobertura_social': ['OBRA SOCIAL DE LA UNION OBRERA METALURGICA DE LA REPUBLICA ARGENTINA', 'O.S.P. CORDOBA (APROSS)'],
        'rnos': ['112103', '999999'],
        'provincia': ['Buenos Aires', 'Cordoba'],
        'departamento': ['Lomas de Zamora', 'Colon'],
        'localidad': ['Temperley', 'Unquillo'],
        'domicilio': ['ORURO 640', 'San Martin 771'],
        'codigo_postal': [1834, 5109],
        'pais_nacimiento': ['Argentina'],
        'nacionalidad': ['Argentina'],
        'fallecido': ['NO', 'SI']
    }
}