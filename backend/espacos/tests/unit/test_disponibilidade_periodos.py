# ===============================================================
# Título: Testes dos períodos de disponibilidade do espaço
# Descrição: Cobre Espaco.aplicar_periodo (ligar e desligar manhã, tarde,
#            noite e finais de semana em horarios_semana) e os checkboxes
#            de disponibilidade do EspacoForm, que antes gravavam um campo
#            inexistente e por isso nunca persistiam.
# Autor: Will
# Data: 19/10/2026
# ===============================================================

import pytest

from espacos.forms import EspacoForm
from espacos.models import Espaco


def espaco_com(horarios):
    """Espaço em memória, só com os horários (os métodos não usam o banco)"""
    return Espaco(horarios_semana=horarios)


# ===============================================================
# MODELO: aplicar_periodo
# ===============================================================

class TestAplicarPeriodoLigando:

    def test_liga_manha_com_horario_padrao_em_dias_uteis(self):
        espaco = espaco_com({})

        espaco.aplicar_periodo('manha', True)

        assert set(espaco.horarios_semana) == {
            'segunda', 'terca', 'quarta', 'quinta', 'sexta'
        }
        assert espaco.horarios_semana['segunda'] == [
            {'inicio': '08:00', 'fim': '12:00'}
        ]
        assert espaco.atende_no_periodo('manha')

    def test_liga_noite_e_tarde(self):
        espaco = espaco_com({})

        espaco.aplicar_periodo('tarde', True)
        espaco.aplicar_periodo('noite', True)

        assert espaco.atende_no_periodo('tarde')
        assert espaco.atende_no_periodo('noite')
        assert not espaco.atende_no_periodo('manha')

    def test_liga_finais_de_semana_em_sabado_e_domingo(self):
        espaco = espaco_com({})

        espaco.aplicar_periodo('finais_de_semana', True)

        assert set(espaco.horarios_semana) == {'sabado', 'domingo'}
        assert espaco.atende_no_periodo('finais_de_semana')

    def test_periodo_ja_atendido_nao_muda_nada(self):
        original = {'segunda': [{'inicio': '09:00', 'fim': '11:00'}]}
        espaco = espaco_com(original)

        espaco.aplicar_periodo('manha', True)

        assert espaco.horarios_semana == original

    def test_nao_apaga_horarios_de_outros_periodos(self):
        espaco = espaco_com({'segunda': [{'inicio': '19:00', 'fim': '21:00'}]})

        espaco.aplicar_periodo('manha', True)

        assert {'inicio': '19:00', 'fim': '21:00'} in espaco.horarios_semana['segunda']
        assert {'inicio': '08:00', 'fim': '12:00'} in espaco.horarios_semana['segunda']

    def test_horarios_vazios_ou_none_nao_quebram(self):
        espaco = espaco_com({'segunda': None, 'terca': []})

        espaco.aplicar_periodo('noite', True)

        assert espaco.atende_no_periodo('noite')


class TestAplicarPeriodoDesligando:

    def test_desliga_manha_remove_horario_inteiro_dentro_da_faixa(self):
        espaco = espaco_com({'segunda': [{'inicio': '08:00', 'fim': '12:00'}]})

        espaco.aplicar_periodo('manha', False)

        assert espaco.horarios_semana == {}

    def test_desliga_manha_recorta_horario_que_atravessa_a_faixa(self):
        espaco = espaco_com({'segunda': [{'inicio': '09:00', 'fim': '17:00'}]})

        espaco.aplicar_periodo('manha', False)

        assert espaco.horarios_semana == {
            'segunda': [{'inicio': '12:00', 'fim': '17:00'}]
        }
        assert not espaco.atende_no_periodo('manha')
        assert espaco.atende_no_periodo('tarde')

    def test_desliga_tarde_divide_horario_que_cobre_a_faixa_toda(self):
        espaco = espaco_com({'segunda': [{'inicio': '08:00', 'fim': '20:00'}]})

        espaco.aplicar_periodo('tarde', False)

        assert espaco.horarios_semana['segunda'] == [
            {'inicio': '08:00', 'fim': '12:00'},
            {'inicio': '18:00', 'fim': '20:00'},
        ]
        assert not espaco.atende_no_periodo('tarde')

    def test_desliga_noite_recorta_o_fim_em_24h(self):
        espaco = espaco_com({'sexta': [{'inicio': '16:00', 'fim': '23:59'}]})

        espaco.aplicar_periodo('noite', False)

        assert espaco.horarios_semana == {
            'sexta': [{'inicio': '16:00', 'fim': '18:00'}]
        }

    def test_desliga_noite_em_horario_que_passa_da_meia_noite(self):
        espaco = espaco_com({'sexta': [{'inicio': '20:00', 'fim': '02:00'}]})

        espaco.aplicar_periodo('noite', False)

        # Só sobra a parte depois da meia-noite, que pertence à manhã
        assert espaco.horarios_semana == {
            'sexta': [{'inicio': '00:00', 'fim': '02:00'}]
        }

    def test_horario_fora_da_faixa_permanece(self):
        espaco = espaco_com({'segunda': [{'inicio': '14:00', 'fim': '16:00'}]})

        espaco.aplicar_periodo('manha', False)

        assert espaco.horarios_semana == {
            'segunda': [{'inicio': '14:00', 'fim': '16:00'}]
        }

    def test_desliga_finais_de_semana_remove_sabado_e_domingo(self):
        espaco = espaco_com({
            'segunda': [{'inicio': '08:00', 'fim': '12:00'}],
            'sabado': [{'inicio': '08:00', 'fim': '18:00'}],
            'domingo': [{'inicio': '09:00', 'fim': '13:00'}],
        })

        espaco.aplicar_periodo('finais_de_semana', False)

        assert set(espaco.horarios_semana) == {'segunda'}

    def test_dado_fora_do_padrao_e_preservado(self):
        estranho = {'inicio': 'abc', 'fim': 'xyz'}
        espaco = espaco_com({'segunda': [estranho]})

        espaco.aplicar_periodo('manha', False)

        assert espaco.horarios_semana == {'segunda': [estranho]}

    def test_nao_altera_o_dicionario_original(self):
        original = {'segunda': [{'inicio': '08:00', 'fim': '12:00'}]}
        espaco = espaco_com(original)

        espaco.aplicar_periodo('manha', False)

        assert original == {'segunda': [{'inicio': '08:00', 'fim': '12:00'}]}


# ===============================================================
# FORMULÁRIO: checkboxes de disponibilidade
# ===============================================================

DADOS_BASE = {
    'nome': 'Espaço Períodos', 'descricao_breve': 'Breve',
    'cep': '20040020', 'bairro': 'Centro', 'tipo_espaco': 'clinica',
    'email': 'contato@periodos.com', 'cidade_texto': 'Lisboa',
}


@pytest.fixture
def espaco_salvo(db, django_user_model):
    dono = django_user_model.objects.create_user(
        username='dono_periodos', email='dp@form.com', password='senha123'
    )
    return Espaco.objects.create(
        nome='Espaço Períodos', slug='espaco-periodos',
        descricao_breve='b', descricao_completa='c', endereco='Rua',
        cep='20040-020', bairro='Centro', tipo_espaco='clinica',
        cidade_texto='Lisboa', responsavel=dono, is_active=True,
        horarios_semana={'segunda': [{'inicio': '09:00', 'fim': '17:00'}]},
    )


@pytest.mark.django_db
class TestCheckboxesDeDisponibilidade:

    def test_ao_editar_os_checkboxes_refletem_os_horarios(self, espaco_salvo):
        form = EspacoForm(instance=espaco_salvo)

        assert form.fields['disponibilidade_manha'].initial is True
        assert form.fields['disponibilidade_tarde'].initial is True
        assert form.fields['disponibilidade_noite'].initial is False
        assert form.fields['disponibilidade_finais_semana'].initial is False

    def test_marcar_noite_persiste_no_banco(self, espaco_salvo):
        form = EspacoForm(
            data={**DADOS_BASE, 'disponibilidade_manha': 'on',
                  'disponibilidade_tarde': 'on', 'disponibilidade_noite': 'on'},
            instance=espaco_salvo,
        )

        assert form.is_valid(), form.errors
        form.save()

        espaco_salvo.refresh_from_db()
        assert espaco_salvo.atende_no_periodo('noite')
        # O horário detalhado que já existia continua lá
        assert {'inicio': '09:00', 'fim': '17:00'} in espaco_salvo.horarios_semana['segunda']

    def test_desmarcar_manha_recorta_e_persiste(self, espaco_salvo):
        form = EspacoForm(
            data={**DADOS_BASE, 'disponibilidade_tarde': 'on'},
            instance=espaco_salvo,
        )

        assert form.is_valid(), form.errors
        form.save()

        espaco_salvo.refresh_from_db()
        assert not espaco_salvo.atende_no_periodo('manha')
        assert espaco_salvo.horarios_semana['segunda'] == [
            {'inicio': '12:00', 'fim': '17:00'}
        ]

    def test_sem_mexer_nos_checkboxes_os_horarios_nao_mudam(self, espaco_salvo):
        original = dict(espaco_salvo.horarios_semana)
        form = EspacoForm(
            data={**DADOS_BASE, 'disponibilidade_manha': 'on',
                  'disponibilidade_tarde': 'on'},
            instance=espaco_salvo,
        )

        assert form.is_valid(), form.errors
        form.save()

        espaco_salvo.refresh_from_db()
        assert espaco_salvo.horarios_semana == original

    def test_marcar_finais_de_semana_persiste(self, espaco_salvo):
        form = EspacoForm(
            data={**DADOS_BASE, 'disponibilidade_manha': 'on',
                  'disponibilidade_tarde': 'on',
                  'disponibilidade_finais_semana': 'on'},
            instance=espaco_salvo,
        )

        assert form.is_valid(), form.errors
        form.save()

        espaco_salvo.refresh_from_db()
        assert espaco_salvo.atende_no_periodo('finais_de_semana')
