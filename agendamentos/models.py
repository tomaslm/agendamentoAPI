from django.db import models
from django.core.validators import ValidationError


class Agendamento(models.Model):
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    paciente = models.CharField(max_length=200)
    procedimento = models.CharField(max_length=200)

    def __str__(self):
        return str(self.data_inicio) + ', ' + str(self.data_fim) + ', ' + self.paciente + ', ' + self.procedimento
