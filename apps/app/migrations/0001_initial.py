# Generated by Django 5.1.2 on 2024-10-21 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_categoria', models.CharField(max_length=100, unique=True)),
                ('cor_categoria', models.CharField(default='#FFFFFF', max_length=7)),
                ('imagem', models.CharField(blank=True, max_length=250, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('deletavel', models.BooleanField(default=True)),
                ('editavel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusRotina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_status', models.CharField(max_length=100, unique=True)),
                ('cor_status', models.CharField(default='#FFFFFF', max_length=7)),
                ('deletavel', models.BooleanField(default=True)),
                ('editavel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=100, unique=True)),
                ('imagem', models.CharField(blank=True, max_length=250, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('categoria', models.ForeignKey(default='SEM_CATEGORIA', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.categoriaproduto')),
            ],
        ),
        migrations.CreateModel(
            name='RotinaDeCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_de_compra', models.CharField(blank=True, max_length=250, null=True)),
                ('iniciada_em', models.DateTimeField(auto_now_add=True)),
                ('finalizada_em', models.DateTimeField(blank=True, null=True)),
                ('valor_total', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status_rotina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.statusrotina')),
            ],
        ),
        migrations.CreateModel(
            name='FluxoDeRotina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('quant_produto', models.FloatField(default=0.0)),
                ('valor_produto', models.FloatField(default=0.0)),
                ('valor_total_produto', models.FloatField(default=0.0)),
                ('produto', models.ForeignKey(default='PRODUTO_DELETADO', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.produto')),
                ('rotina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.rotinadecompra')),
            ],
        ),
    ]