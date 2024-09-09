# Generated by Django 5.1 on 2024-09-02 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orgao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=20, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_vigencia_inicial', models.DateField()),
                ('data_vigencia_final', models.DateField()),
                ('razao_social_fornecedor', models.CharField(max_length=255)),
                ('objeto', models.TextField()),
                ('valor_inicial', models.DecimalField(decimal_places=2, max_digits=15)),
                ('orgao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to='nutis.orgao')),
            ],
        ),
    ]
