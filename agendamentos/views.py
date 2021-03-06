from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Agendamento
from .serializers import AgendamentoSerializer
from rest_framework.settings import api_settings
from django.db.models import Q


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
        serializer = AgendamentoSerializer(agendamento, data=request.data)
        if serializer.is_valid():
            try:
                serializer.validate_agendamento_com_mesmo_horario(
                    request.data, pk)
            except serializers.ValidationError as ex:
                return Response(str(ex), status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_agendamentos(request):
    if request.method == 'GET':
        paginator_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = paginator_class()

        queryset = Agendamento.objects.all()
        query_filtro_global = request.GET.get('q')
        if query_filtro_global:
            queryset = queryset.filter(
                Q(paciente__icontains=query_filtro_global) | Q(procedimento__icontains=query_filtro_global))

        sort = request.GET.get('sort')
        if sort:
            if sort == "data_hora_inicio":
                queryset = queryset.order_by('data', 'hora_inicio')
            elif sort == "-data_hora_inicio":
                queryset = queryset.order_by('-data', '-hora_inicio')
            elif sort == "data_hora_fim":
                queryset = queryset.order_by('data', 'hora_fim')
            elif sort == "-data_hora_fim":
                queryset = queryset.order_by('-data', '-hora_fim')
            else:
                queryset = queryset.order_by(sort)

        page = paginator.paginate_queryset(queryset, request)

        serializer = AgendamentoSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        data = {
            'data': request.data.get('data'),
            'hora_inicio': request.data.get('hora_inicio'),
            'hora_fim': request.data.get('hora_fim'),
            'paciente': request.data.get('paciente'),
            'procedimento': request.data.get('procedimento'),
        }
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.validate_agendamento_com_mesmo_horario(data, 0)
            except serializers.ValidationError as ex:
                return Response(str(ex), status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
