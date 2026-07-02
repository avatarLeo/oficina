from django.db import migrations, models


def atualizar_status(apps, schema_editor):
    Servico = apps.get_model('servico', 'Servico')
    HistoricoStatus = apps.get_model('servico', 'HistoricoStatus')

    Servico.objects.filter(status='aguardando_peca').update(status='aguardando')
    HistoricoStatus.objects.filter(status_novo='aguardando_peca').update(status_novo='aguardando')
    HistoricoStatus.objects.filter(status_anterior='aguardando_peca').update(status_anterior='aguardando')


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0009_backfill_previsao_entrega'),
    ]

    operations = [
        migrations.RunPython(atualizar_status),
        migrations.AlterField(
            model_name='servico',
            name='status',
            field=models.CharField(choices=[('aguardando', 'Aguardando'), ('em_andamento', 'Em andamento'), ('servico_concluido', 'Serviço concluído')], default='aguardando', max_length=20),
        ),
    ]
