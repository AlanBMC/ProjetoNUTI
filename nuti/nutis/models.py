from django.db import models
from django.utils import timezone

# Create your models here.

class Orgao(models.Model):
    cnpj = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
    
class Contrato(models.Model):
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE, related_name='contratos')
    data_vigencia_inicial = models.DateField()
    data_vigencia_final = models.DateField()
    razao_social_fornecedor = models.CharField(max_length=255)
    objeto = models.TextField()
    valor_inicial = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Contrato {self.objeto} - {self.orgao.nome}'