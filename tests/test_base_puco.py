from sisa.puco import Puco
from sisa import settings


def test_test_data():
    for r in range(1, 8):

        puco = Puco(dni='11111111')
        resp = puco.get_info_ciudadano()
        assert resp['ok']
        if resp['ok']:
            if resp['persona_encontrada']:
                assert puco.cobertura_social in settings.test_data['puco']['cobertura_social']
                assert puco.denominacion in settings.test_data['puco']['denominacion']
                assert puco.rnos in settings.test_data['puco']['rnos']
                assert puco.tipo_doc in settings.test_data['puco']['tipo_doc']
                print(f'{r} OK PUCO {puco}')
            else:
                print(f'{r} No encontrada')

        