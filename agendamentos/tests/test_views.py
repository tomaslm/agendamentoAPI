import json
from rest_framework import status
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from ..models import Agendamento
from ..serializers import AgendamentoSerializer
import datetime
import pytz

client = Client()


class BuscaTodosAgendamentosTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.jose = Agendamento.objects.create(
            paciente='Jose', procedimento='Availiação',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.marcio = Agendamento.objects.create(
            paciente='Marcio', procedimento='Retorno',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())

    def test_get_all_atendimentos(self):
        response = client.get(reverse('get_post_agendamentos'))
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BuscaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.jose = Agendamento.objects.create(
            paciente='Jose', procedimento='Availiação',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.marcio = Agendamento.objects.create(
            paciente='Marcio', procedimento='Retorno',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())

    def test_get_atendimento_com_id_invalido(self):
        response = client.get(
            reverse('get_delete_update_agendamento', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_atendimento_com_id_valido(self):
        response = client.get(
            reverse('get_delete_update_agendamento', kwargs={'pk': self.joana.pk}))
        serializer = AgendamentoSerializer(self.joana)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CriaAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Retorno',
            data=datetime.datetime(2018, 1, 1, 10, 30, 0,
                                   0, tzinfo=pytz.timezone('America/Sao_Paulo')).date(),
            hora_inicio=datetime.datetime(
                2018, 1, 1, 10, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time(),
            hora_fim=datetime.datetime(
                2018, 1, 1, 11, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time())
        self.payload_valido = {
            'data': '2018-01-09',
            'hora_inicio': '09:00:00.000',
            'hora_fim': '09:50:00.000',
            'paciente': 'Jose',
            'procedimento': 'Cirurgia'
        }

        self.payload_invalido = {
            'data': '2018-01-09',
            'hora_inicio': '09:00:00.000',
            'hora_fim': '09:50:00.000',
            'paciente': '',
            'procedimento': 'Cirurgia'
        }
        self.payload_conflitante = {
            'data': '2018-01-01',
            'hora_inicio': '10:00:00.000',
            'hora_fim': '10:50:00.000',
            'paciente': 'Joana',
            'procedimento': 'Cirurgia'
        }
        self.payload_valido_horario_proximo_1 = {
            'data': '2018-01-01',
            'hora_inicio': '10:00:00.000',
            'hora_fim': '10:29:00.000',
            'paciente': 'Joana',
            'procedimento': 'Retorno 2'
        }
        self.payload_valido_horario_proximo_2 = {
            'data': '2018-01-01',
            'hora_inicio': '11:31:00.000',
            'hora_fim': '12:00:00.000',
            'paciente': 'Joana',
            'procedimento': 'Retorno 3'
        }
        self.payload_invalido_horario = {
            'data': '2018-01-01',
            'hora_inicio': '11:00:00.000',
            'hora_fim': '10:00:00.000',
            'paciente': 'José',
            'procedimento': 'Cirurgia'
        }

    def test_cria_agendamento_valido(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_valido),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_201_CREATED)

    def test_cria_agendamento_invalido(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_invalido),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_cria_agendamento_valido_horario_proximo_1(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_valido_horario_proximo_1),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_201_CREATED)

    def test_cria_agendamento_valido_horario_proximo_2(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_valido_horario_proximo_2),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_201_CREATED)

    def test_cria_agendamento_invalido_horario(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_invalido_horario),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_cria_agendamento_conflitante(self):
        response = client.post(
            reverse('get_post_agendamentos'),
            data=json.dumps(self.payload_conflitante),
            content_type='application/json',
        )
        self.assertEqual(response.status_code,  status.HTTP_409_CONFLICT)


class AtualizaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data=timezone.now().date(), hora_inicio=timezone.now().time(), hora_fim=timezone.now().time())
        self.jose_cirurgia = Agendamento.objects.create(
            paciente='Jose', procedimento='Cirurgia',
            data=datetime.datetime(2018, 1, 1, 10, 30, 0,
                                   0, tzinfo=pytz.timezone('America/Sao_Paulo')).date(),
            hora_inicio=datetime.datetime(
                2018, 1, 1, 10, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time(),
            hora_fim=datetime.datetime(
                2018, 1, 1, 11, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time())
        self.jose_retorno = Agendamento.objects.create(
            paciente='Jose', procedimento='Retorno',
            data=datetime.datetime(2018, 1, 1, 10, 30, 0,
                                   0, tzinfo=pytz.timezone('America/Sao_Paulo')).date(),
            hora_inicio=datetime.datetime(
                2018, 1, 2, 10, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time(),
            hora_fim=datetime.datetime(
                2018, 1, 2, 11, 30, 0, 0, tzinfo=pytz.timezone('America/Sao_Paulo')).time())
        self.payload_valido = {
            'data': '2018-01-09',
            'hora_inicio': '09:00:00.000',
            'hora_fim': '09:50:00.000',
            'paciente': 'Joana',
            'procedimento': 'Cirurgia'
        }

        self.payload_invalido = {
            'data': '2018-01-09',
            'hora_inicio': '09:00:00.000',
            'hora_fim': '09:50:00.000',
            'paciente': '',
            'procedimento': 'Cirurgia'
        }
        self.payload_conflitante = {
            'data': '2018-01-01',
            'hora_inicio': '10:35:00.000',
            'hora_fim': '11:25:00.000',
            'paciente': 'Jose',
            'procedimento': 'Retorno'
        }
        self.payload_invalido_horario = {
            'data': '2018-01-09',
            'hora_inicio': '11:00:00.000',
            'hora_fim': '10:00:00.000',
            'paciente': '',
            'procedimento': 'Cirurgia'
        }

    def test_atualiza_agendamento_valido(self):
        response = client.put(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': self.joana.pk}),
            data=json.dumps(self.payload_valido),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_204_NO_CONTENT)

    def test_atualiza_agendamento_invalido(self):
        response = client.put(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': self.joana.pk}),
            data=json.dumps(self.payload_invalido),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_atualiza_agendamento_invalido_horario(self):
        response = client.put(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': self.joana.pk}),
            data=json.dumps(self.payload_invalido_horario),
            content_type='application/json',
        )

        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_atualiza_agendamento_conflitante(self):
        response = client.put(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': self.jose_retorno.pk}),
            data=json.dumps(self.payload_conflitante),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class DeletaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())

    def teste_deleta_agendamento_valido(self):
        response = client.delete(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': self.joana.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def teste_deleta_agendamento_invalido(self):
        response = client.delete(
            reverse('get_delete_update_agendamento',
                    kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
