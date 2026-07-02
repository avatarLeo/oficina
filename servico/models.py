from datetime import timedelta
from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.nome} ({self.cpf or self.telefone})'


class Servico(models.Model):
    class Status(models.TextChoices):
        AGUARDANDO = 'aguardando', 'Aguardando'
        EM_ANDAMENTO = 'em_andamento', 'Em andamento'
        SERVICO_CONCLUIDO = 'servico_concluido', 'Serviço concluído'

    class Pagamento(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PARCIAL = 'parcial', 'Parcial'
        PAGO = 'pago', 'Pago'

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='servicos'
    )
    descricao = models.TextField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AGUARDANDO
    )
    previsao_entrega = models.DateField(null=True, blank=True, verbose_name='Previsão de entrega')
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_pagamento = models.CharField(
        max_length=20, choices=Pagamento.choices, default=Pagamento.PENDENTE, editable=False
    )
    imagem = models.ImageField(upload_to='servico/imgs/%Y/%m/%d/', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-atualizado_em']

    def save(self, *args, **kwargs):
        if self.previsao_entrega is None:
            self.previsao_entrega = timezone.now().date() + timedelta(days=4)
        if self.preco is not None and self.valor_pago >= self.preco:
            self.status_pagamento = self.Pagamento.PAGO
        elif self.valor_pago > 0:
            self.status_pagamento = self.Pagamento.PARCIAL
        else:
            self.status_pagamento = self.Pagamento.PENDENTE
        super().save(*args, **kwargs)

    @property
    def restante(self):
        if self.preco is not None:
            return self.preco - self.valor_pago
        return None

    def __str__(self):
        return f'{self.cliente.nome} — {self.get_status_display()}'


class HistoricoStatus(models.Model):
    servico = models.ForeignKey(
        Servico, on_delete=models.CASCADE, related_name='historico'
    )
    status_anterior = models.CharField(max_length=20, blank=True)
    status_novo = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Histórico de status'
        verbose_name_plural = 'Históricos de status'

    def __str__(self):
        return f'{self.servico}: {self.status_anterior} → {self.status_novo}'


class ServicoOferta(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=10, default='🛠️')
    ordem = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordem']
        verbose_name = 'Serviço oferecido'
        verbose_name_plural = 'Serviços oferecidos'

    def __str__(self):
        return self.titulo
