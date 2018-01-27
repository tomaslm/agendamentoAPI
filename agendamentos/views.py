from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Agendamento
from .serializers import AgendamentoSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_agendamento(request, pk):
    try:
        agendamento = Agendamento.objects.get(pk=pk)
    except Agendamento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AgendamentoSerializer(agendamento)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        agendamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_agendamentos(request):
    if request.method == 'GET':
        # verificar paginacao
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'data_inicio': request.data.get('data_inicio'),
            'data_fim': request.data.get('data_fim'),
            'paciente': request.data.get('paciente'),
            'procedimento': request.data.get('procedimento'),
        }
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
