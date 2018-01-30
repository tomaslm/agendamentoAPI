from django.db import models
from django.core.validators import ValidationError


class Agendamento(models.Model):
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    paciente = models.CharField(max_length=200)
    procedimento = models.CharField(max_length=200)

    def __str__(self):
        return str(self.data) + ', ' + str(self.hora_inicio) + ', ' + str(self.hora_fim) + ', ' + self.paciente + ', ' + self.procedimento
