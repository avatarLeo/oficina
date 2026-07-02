from django.contrib import admin
from django.urls import path
from servico.views import (
    home, acompanhar,
    dashboard_home, dashboard_servicos,
    dashboard_servico_detail, dashboard_mudar_status,
    dashboard_adicionar_observacao, dashboard_registrar_pagamento,
    dashboard_alterar_previsao,
    dashboard_add_cliente, dashboard_add_servico,
    dashboard_editar_servico, dashboard_excluir_servico,
    dashboard_clientes, dashboard_cliente_detail,
    dashboard_editar_cliente, dashboard_excluir_cliente,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public
    path('', home),
    path('acompanhar/', acompanhar, name='acompanhar'),

    # Dashboard
    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('dashboard/servicos/', dashboard_servicos, name='dashboard_servicos'),
    path('dashboard/servico/<int:servico_id>/', dashboard_servico_detail, name='dashboard_servico_detail'),
    path('dashboard/servico/<int:servico_id>/status/', dashboard_mudar_status, name='dashboard_mudar_status'),
    path('dashboard/servico/<int:servico_id>/observacao/', dashboard_adicionar_observacao, name='dashboard_adicionar_observacao'),
    path('dashboard/servico/<int:servico_id>/pagamento/', dashboard_registrar_pagamento, name='dashboard_registrar_pagamento'),
    path('dashboard/servico/<int:servico_id>/previsao/', dashboard_alterar_previsao, name='dashboard_alterar_previsao'),
    path('dashboard/clientes/', dashboard_clientes, name='dashboard_clientes'),
    path('dashboard/clientes/novo/', dashboard_add_cliente, name='dashboard_add_cliente'),
    path('dashboard/cliente/<int:cliente_id>/', dashboard_cliente_detail, name='dashboard_cliente_detail'),
    path('dashboard/cliente/<int:cliente_id>/editar/', dashboard_editar_cliente, name='dashboard_editar_cliente'),
    path('dashboard/cliente/<int:cliente_id>/excluir/', dashboard_excluir_cliente, name='dashboard_excluir_cliente'),
    path('dashboard/servicos/novo/', dashboard_add_servico, name='dashboard_add_servico'),
    path('dashboard/servico/<int:servico_id>/editar/', dashboard_editar_servico, name='dashboard_editar_servico'),
    path('dashboard/servico/<int:servico_id>/excluir/', dashboard_excluir_servico, name='dashboard_excluir_servico'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
