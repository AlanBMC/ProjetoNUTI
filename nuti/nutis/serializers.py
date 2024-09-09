from rest_framework import serializers

class ConsultaContratoSerializer(serializers.Serializer):
    datainicio = serializers.DateField(required=True, format='%Y-%m-%d')
    datafim = serializers.DateField(required=True, format='%Y-%m-%d')
    cnpj = serializers.CharField(required=True, max_length=14, min_length=14)

    