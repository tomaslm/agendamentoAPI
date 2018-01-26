import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Agendamento

class AgendamentoModelTests(TestCase):
	
	def test_(self):
		self.assertIs(False,False)