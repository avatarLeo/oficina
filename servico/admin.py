from django.contrib import admin
from .models import Cliente, Servico, HistoricoStatus, ServicoOferta


class HistoricoInline(admin.TabularInline):
    model = HistoricoStatus
    extra = 0
    readonly_fields = ('status_anterior', 'status_novo', 'criado_em')
    can_delete = False
    verbose_name = 'Histórico'
    verbose_name_plural = 'Histórico de status'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'quant_servicos', 'criado_em')
    search_fields = ('nome', 'cpf', 'telefone')
    list_per_page = 25

    def quant_servicos(self, obj):
        return obj.servicos.count()
    quant_servicos.short_description = 'Serviços'


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'descricao_curta', 'status', 'previsao_entrega', 'status_pagamento', 'preco', 'dias_em_espera', 'criado_em')
    list_filter = ('status', 'status_pagamento', 'previsao_entrega', 'criado_em')
    search_fields = ('cliente__nome', 'cliente__cpf', 'descricao')
    list_per_page = 25
    inlines = [HistoricoInline]
    fieldsets = (
        (None, {'fields': ('cliente', 'descricao', 'observacoes', 'status', 'previsao_entrega', 'imagem')}),
        ('Pagamento', {'fields': ('preco', 'valor_pago', 'status_pagamento')}),
    )
    readonly_fields = ('status_pagamento',)

    def descricao_curta(self, obj):
        return obj.descricao[:60] + '...' if len(obj.descricao) > 60 else obj.descricao
    descricao_curta.short_description = 'Descrição'

    def dias_em_espera(self, obj):
        delta = obj.atualizado_em - obj.criado_em
        return delta.days
    dias_em_espera.short_description = 'Dias'


@admin.register(ServicoOferta)
class ServicoOfertaAdmin(admin.ModelAdmin):
    list_display = ('icone', 'titulo', 'ordem')
    list_editable = ('ordem',)
    search_fields = ('titulo',)
