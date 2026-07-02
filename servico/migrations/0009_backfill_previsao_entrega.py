from datetime import timedelta
from django.db import migrations


def backfill_previsao(apps, schema_editor):
    Servico = apps.get_model('servico', 'Servico')
    for servico in Servico.objects.filter(previsao_entrega__isnull=True):
        servico.previsao_entrega = servico.criado_em.date() + timedelta(days=4)
        servico.save(update_fields=['previsao_entrega'])


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0008_servico_previsao_entrega'),
    ]

    operations = [
        migrations.RunPython(backfill_previsao),
    ]
