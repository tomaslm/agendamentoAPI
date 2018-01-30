from rest_framework import serializers
from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ('data_inicio', 'data_fim', 'paciente', 'procedimento')

    def validate_agendamento_com_mesmo_horario(self, data, pk):
        print(data)
        print(pk)
        agendamentos_com_mesmo_horario = Agendamento.objects.filter(
            paciente=data['paciente'],
            data_inicio__lte=data['data_fim'],
            data_fim__gt=data['data_inicio']).exclude(pk=pk)
        if agendamentos_com_mesmo_horario.exists():
            raise serializers.ValidationError(
                'Conflito de data para o agendamento deste paciente')
        return data
