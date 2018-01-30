from django.utils import timezone

from django.utils import timezone
from django.test import TestCase

from ..models import Agendamento


class AgendamentoModelTests(TestCase):

    def setUp(self):
        Agendamento.objects.create(
            paciente='Joana', procedimento='Cirurgia',
            data=timezone.now().date(), hora_inicio=timezone.now().time(),
            hora_fim=timezone.now().time())

    def test_procedimento_joana(self):
        agendamento_teste = Agendamento.objects.get(paciente='Joana')
        self.assertEqual('Cirurgia', agendamento_teste.procedimento)
