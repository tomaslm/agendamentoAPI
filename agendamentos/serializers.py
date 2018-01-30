from rest_framework import serializers
from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ('data', 'hora_inicio', 'hora_fim',
                  'paciente', 'procedimento')

    def validate(self, data):
        if data['hora_inicio'] > data['hora_fim']:
            raise serializers.ValidationError(
                "O horário fim deve ser posterior ao horário início")
        return data

    def validate_agendamento_com_mesmo_horario(self, data, pk):
        agendamentos_com_mesmo_horario = Agendamento.objects.filter(
            paciente=data['paciente'],
            data=data['data'],
            hora_inicio__lt=data['hora_fim'],  # comeca antes do fim
            hora_fim__gt=data['hora_inicio']  # acaba depois do inicio
        ).exclude(pk=pk)    # não é o mesmo registro
        if agendamentos_com_mesmo_horario.exists():
            raise serializers.ValidationError(
                'Conflito de data para o agendamento deste paciente')
        return data
