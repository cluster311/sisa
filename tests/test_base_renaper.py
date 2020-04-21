from sisa.renaper import Renaper
from sisa import settings


def test_test_data():
    for r in range(1, 8):
        rena = Renaper(dni='111111111')
        resp = rena.get_info_ciudadano()
        assert resp['ok']
        if resp['ok']:
            if resp['persona_encontrada']:
                assert rena.codigo_sisa in settings.test_data['renaper']['codigo_sisa']
                assert rena.codigo_renaper in settings.test_data['renaper']['codigo_renaper']
                assert rena.tipo_doc in settings.test_data['renaper']['tipo_doc']
                assert rena.apellido in settings.test_data['renaper']['apellido']
                assert rena.nombre in settings.test_data['renaper']['nombre']
                assert rena.sexo in settings.test_data['renaper']['sexo']
                assert rena.fecha_nacimiento in settings.test_data['renaper']['fecha_nacimiento']
                assert rena.estado_civil in settings.test_data['renaper']['estado_civil']
                assert rena.tipo_cobertura_vigente in settings.test_data['renaper']['tipo_cobertura_vigente']
                assert rena.cobertura_social in settings.test_data['renaper']['cobertura_social']
                assert rena.rnos in settings.test_data['renaper']['rnos']
                assert rena.provincia in settings.test_data['renaper']['provincia']
                assert rena.departamento in settings.test_data['renaper']['departamento']
                assert rena.localidad in settings.test_data['renaper']['localidad']
                assert rena.domicilio in settings.test_data['renaper']['domicilio']
                assert rena.codigo_postal in settings.test_data['renaper']['codigo_postal']
                assert rena.pais_nacimiento in settings.test_data['renaper']['pais_nacimiento']
                assert rena.nacionalidad in settings.test_data['renaper']['nacionalidad']
                assert rena.fallecido in settings.test_data['renaper']['fallecido']
                print(f'{r} OK PUCO {rena}')
            else:
                print(f'{r} No encontrada')
        