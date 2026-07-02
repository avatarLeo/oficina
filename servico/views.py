from decimal import Decimal
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.http import HttpResponse
from .models import Servico, Cliente, HistoricoStatus, ServicoOferta


def home(request):
    ofertas = ServicoOferta.objects.all()
    return render(request, 'servico/pages/home.html', context={
        'ofertas': ofertas
    })


def acompanhar(request):
    query = request.GET.get('query', '').strip()
    cliente = None
    servicos = []

    if query:
        cliente = Cliente.objects.filter(
            models.Q(cpf=query) | models.Q(telefone=query)
        ).first()
        if cliente:
            servicos = cliente.servicos.all()

    return render(request, 'servico/pages/acompanhar.html', context={
        'query': query,
        'cliente': cliente,
        'servicos': servicos,
    })


def _staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_home(request):
    total = Servico.objects.count()
    aguardando = Servico.objects.filter(status=Servico.Status.AGUARDANDO).count()
    andamento = Servico.objects.filter(status=Servico.Status.EM_ANDAMENTO).count()
    concluidos = Servico.objects.filter(status=Servico.Status.SERVICO_CONCLUIDO).count()
    atrasados = Servico.objects.filter(
        previsao_entrega__lt=date.today()
    ).exclude(status=Servico.Status.SERVICO_CONCLUIDO).count()
    nao_pagos = Servico.objects.exclude(
        status_pagamento=Servico.Pagamento.PAGO
    ).count()

    return render(request, 'servico/dashboard/home.html', context={
        'total': total,
        'aguardando': aguardando,
        'andamento': andamento,
        'concluidos': concluidos,
        'atrasados': atrasados,
        'nao_pagos': nao_pagos,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_servicos(request):
    servicos = Servico.objects.select_related('cliente').order_by('previsao_entrega')
    status_filtro = request.GET.get('status', '')

    if request.GET.get('atrasado'):
        servicos = servicos.filter(
            previsao_entrega__lt=date.today()
        ).exclude(status=Servico.Status.SERVICO_CONCLUIDO)
    elif request.GET.get('nao_pago'):
        servicos = servicos.exclude(status_pagamento=Servico.Pagamento.PAGO)
    elif status_filtro:
        servicos = servicos.filter(status=status_filtro)

    return render(request, 'servico/dashboard/servicos.html', context={
        'servicos': servicos,
        'status_atual': status_filtro,
        'today': date.today(),
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_servico_detail(request, servico_id):
    servico = get_object_or_404(
        Servico.objects.select_related('cliente').prefetch_related('historico'),
        id=servico_id
    )
    return render(request, 'servico/dashboard/servico_detail.html', context={
        'servico': servico,
        'today': date.today(),
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_mudar_status(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    novo_status = request.POST.get('status', '')

    if novo_status in dict(Servico.Status.choices):
        status_anterior = servico.status
        servico.status = novo_status
        servico.save()

        HistoricoStatus.objects.create(
            servico=servico,
            status_anterior=status_anterior,
            status_novo=novo_status,
        )

    return redirect('dashboard_servico_detail', servico_id=servico.id)


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_adicionar_observacao(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    texto = request.POST.get('observacao', '').strip()

    if texto:
        observacoes = servico.observacoes
        if observacoes:
            observacoes += '\n\n' + texto
        else:
            observacoes = texto
        servico.observacoes = observacoes
        servico.save()

    return render(request, 'servico/dashboard/partials/observacoes.html', context={
        'servico': servico,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_registrar_pagamento(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    valor = request.POST.get('valor', '').strip()

    if valor:
        try:
            valor = Decimal(str(valor).replace(',', '.'))
            if valor > 0:
                servico.valor_pago += valor
                servico.save()
        except (ValueError, TypeError, ArithmeticError):
            pass

    return render(request, 'servico/dashboard/partials/pagamento_card.html', context={
        'servico': Servico.objects.get(id=servico_id),
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_alterar_previsao(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    nova_data = request.POST.get('previsao_entrega', '').strip()

    if nova_data:
        try:
            servico.previsao_entrega = datetime.strptime(nova_data, '%Y-%m-%d').date()
            servico.save(update_fields=['previsao_entrega'])
        except ValueError:
            pass

    return redirect('dashboard_servico_detail', servico_id=servico.id)


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_add_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        cpf = request.POST.get('cpf', '').strip() or None
        email = request.POST.get('email', '').strip() or ''

        if nome and telefone:
            Cliente.objects.create(nome=nome, telefone=telefone, cpf=cpf, email=email)
            return redirect('dashboard_clientes')

    return render(request, 'servico/dashboard/add_cliente.html')


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_add_servico(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        descricao = request.POST.get('descricao', '').strip()
        observacoes = request.POST.get('observacoes', '').strip()
        previsao = request.POST.get('previsao_entrega', '').strip()
        preco = request.POST.get('preco', '').strip()

        if cliente_id and descricao:
            servico = Servico(
                cliente_id=cliente_id,
                descricao=descricao,
                observacoes=observacoes,
            )
            if previsao:
                servico.previsao_entrega = datetime.strptime(previsao, '%Y-%m-%d').date()
            if preco:
                try:
                    servico.preco = float(preco)
                except ValueError:
                    pass
            servico.save()
            return redirect('dashboard_servicos')

    return render(request, 'servico/dashboard/add_servico.html', context={
        'clientes': clientes,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        descricao = request.POST.get('descricao', '').strip()
        observacoes = request.POST.get('observacoes', '').strip()
        previsao = request.POST.get('previsao_entrega', '').strip()
        preco = request.POST.get('preco', '').strip()

        if cliente_id and descricao:
            servico.cliente_id = cliente_id
            servico.descricao = descricao
            servico.observacoes = observacoes
            if previsao:
                servico.previsao_entrega = datetime.strptime(previsao, '%Y-%m-%d').date()
            if preco:
                try:
                    servico.preco = float(preco)
                except ValueError:
                    pass
            servico.save()
            return redirect('dashboard_servico_detail', servico_id=servico.id)

    return render(request, 'servico/dashboard/editar_servico.html', context={
        'servico': servico,
        'clientes': clientes,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_excluir_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    if request.method == 'POST':
        servico.delete()
    return redirect('dashboard_servicos')


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_clientes(request):
    q = request.GET.get('q', '').strip()
    clientes = Cliente.objects.annotate(
        num_servicos=models.Count('servicos')
    ).order_by('-id')

    if q:
        clientes = clientes.filter(
            models.Q(nome__icontains=q) |
            models.Q(cpf__icontains=q) |
            models.Q(telefone__icontains=q)
        )

    return render(request, 'servico/dashboard/clientes.html', context={
        'clientes': clientes,
        'q': q,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        cpf = request.POST.get('cpf', '').strip() or None
        email = request.POST.get('email', '').strip() or ''

        if nome and telefone:
            cliente.nome = nome
            cliente.telefone = telefone
            cliente.cpf = cpf
            cliente.email = email
            cliente.save()
            return redirect('dashboard_clientes')

    return render(request, 'servico/dashboard/editar_cliente.html', context={
        'cliente': cliente,
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_cliente_detail(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    servicos = cliente.servicos.select_related('cliente').order_by('-criado_em')

    total = servicos.count()
    andamento = servicos.filter(status=Servico.Status.EM_ANDAMENTO).count()
    concluidos = servicos.filter(status=Servico.Status.SERVICO_CONCLUIDO).count()
    atrasados = servicos.filter(
        previsao_entrega__lt=date.today()
    ).exclude(status=Servico.Status.SERVICO_CONCLUIDO).count()

    return render(request, 'servico/dashboard/cliente_detail.html', context={
        'cliente': cliente,
        'servicos': servicos,
        'total': total,
        'andamento': andamento,
        'concluidos': concluidos,
        'atrasados': atrasados,
        'today': date.today(),
    })


@login_required(login_url='/admin/login/')
@user_passes_test(_staff_check, login_url='/admin/login/')
def dashboard_excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
    return redirect('dashboard_clientes')
