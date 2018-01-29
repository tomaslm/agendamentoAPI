from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/agendamento/(?P<pk>[0-9]+)$',
        views.get_delete_update_agendamento,
        name='get_delete_update_agendamento'
    ),
    url(
        r'^api/v1/agendamentos/$',
        views.get_post_agendamentos,
        name='get_post_agendamentos'
    )
]
