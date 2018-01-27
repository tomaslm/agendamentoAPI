from django.utils import timezone

from django.utils import timezone
from django.test import TestCase

from ..models import Agendamento


class AgendamentoModelTests(TestCase):

    def setUp(self):
        Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data_inicio=timezone.now(), data_fim=timezone.now())

    def test_procedimento_joana(self):
        agendamento_teste = Agendamento.objects.get(paciente='Joana')
        self.assertEqual('Cirurgia', agendamento_teste.procedimento)
