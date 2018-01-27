import json
from rest_framework import status
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from ..models import Agendamento
from ..serializers import AgendamentoSerializer

client = Client()


class GetAllAgendamentosTest(TestCase):
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


class GetUmAgendamentoTest(TestCase):
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
            reverse('get_delete_update_agendamento', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_atendimento_com_id_valido(self):
        response = client.get(
            reverse('get_delete_update_agendamento', kwargs={'pk': self.joana.pk}))
        serializer = AgendamentoSerializer(self.joana)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostAgendamentoTest(TestCase):
    def setUp(self):
        self.payload_valido = {
            'data_inicio': '2018-01-09T09:00:00.000',
            'data_fim': '2018-01-09T09:50:00.000',
            'paciente': 'Jose',
            'procedimento': 'Cirurgia'
        }

        self.payload_invalido = {
            'paciente': ''
        }
