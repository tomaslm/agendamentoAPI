import json
from rest_framework import status
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from ..models import Agendamento
from ..serializers import AgendamentoSerializer

client = Client()


class BuscaTodosAgendamentosTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.jose = Agendamento.objects.create(
            paciente='Jose', procedimento='Availiação',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.marcio = Agendamento.objects.create(
            paciente='Marcio', procedimento='Retorno',
            data_inicio=timezone.now(), data_fim=timezone.now())

    def test_get_all_atendimentos(self):
        response = client.get(reverse('get_post_agendamentos'))
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BuscaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.jose = Agendamento.objects.create(
            paciente='Jose', procedimento='Availiação',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.marcio = Agendamento.objects.create(
            paciente='Marcio', procedimento='Retorno',
            data_inicio=timezone.now(), data_fim=timezone.now())

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
        self.payload_valido = {
            'data_inicio': '2018-01-09T09:00:00.000',
            'data_fim': '2018-01-09T09:50:00.000',
            'paciente': 'Jose',
            'procedimento': 'Cirurgia'
        }

        self.payload_invalido = {
            'data_inicio': '2018-01-09T09:00:00.000',
            'data_fim': '2018-01-09T09:50:00.000',
            'paciente': '',
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


class AtualizaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.payload_valido = {
            'data_inicio': '2018-01-09T09:00:00.000',
            'data_fim': '2018-01-09T09:50:00.000',
            'paciente': 'Joana',
            'procedimento': 'Cirurgia'
        }

        self.payload_invalido = {
            'data_inicio': '2018-01-09T09:00:00.000',
            'data_fim': '2018-01-09T09:50:00.000',
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


class DeletaUmAgendamentoTest(TestCase):
    def setUp(self):
        self.joana = Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data_inicio=timezone.now(), data_fim=timezone.now())
        self.maria = Agendamento.objects.create(
            paciente='Maria', procedimento='Atendimento',
            data_inicio=timezone.now(), data_fim=timezone.now())

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
