from django.shortcuts import render
import requests
from .models import Orgao, Contrato
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import ConsultaContratoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HomeAPIView(APIView):
    """
    API responsável por lidar com a consulta de contratos e retornar os dados como resposta JSON.
    """
    @swagger_auto_schema(
            operation_description="Consulta de contratos por CNPJ em intervalo de data de ATE um ano",
            request_body=ConsultaContratoSerializer(),
                    manual_parameters=[
                    openapi.Parameter('datainicio', openapi.IN_QUERY, description="Data de início (YYYY-MM-DD)", type=openapi.TYPE_STRING),
                    openapi.Parameter('datafim', openapi.IN_QUERY, description="Data de fim (YYYY-MM-DD)", type=openapi.TYPE_STRING),
                    openapi.Parameter('cnpj', openapi.IN_QUERY, description="CNPJ do órgão (somente números)", type=openapi.TYPE_STRING),
                    ],
            responses={200: 'Retorna a lista de contratos', 400: 'erro de validação'},
    )
    def get(self, request):
        # Obtendo parâmetros da query string (ex: /api/home/?datainicio=2021-01-01&datafim=2021-12-31)
        data_inicio = request.query_params.get('datainicio')
        data_fim = request.query_params.get('datafim')
        cnpj = request.query_params.get('cnpj')

        if not data_inicio or not data_fim or not cnpj:
            return Response({"error": "Todos os parâmetros (datainicio, datafim, cnpj) são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica de processamento aqui

        return Response({"message": "Consulta realizada com sucesso!"})
    def post(self, request):
        url = "https://pncp.gov.br/api/consulta/v1/contratos"
        serializer = ConsultaContratoSerializer(data=request.data)
        if serializer.is_valid():
            # Se os dados forem válidos, você pode acessá-los com serializer.validated_data
            data_inicio = serializer.validated_data['datainicio']
            data_fim = serializer.validated_data['datafim']
            cnpj_clean = serializer.validated_data['cnpj']

        # Converter as datas para 'yyyyMMdd'
        try:
            data_inicio_formatted = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%Y%m%d')
            data_fim_formatted = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%Y%m%d')
        except ValueError:
            return Response({"error": "Formato de data inválido."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se já existem contratos no banco de dados para o CNPJ e período especificado
        contratos_existentes = Contrato.objects.filter(
            orgao__cnpj=cnpj_clean,
            data_vigencia_inicial__gte=data_inicio,
            data_vigencia_final__lte=data_fim
        )

        if contratos_existentes.exists():
            orgao = contratos_existentes.first().orgao
            valor_total_contratos = sum(contrato.valor_inicial for contrato in contratos_existentes)
            return Response({
                'orgao': orgao.nome,
                'cnpj': orgao.cnpj,
                'contratos': [contrato.objeto for contrato in contratos_existentes],
                'valor_total': valor_total_contratos
            })

        # Se não há dados no banco, fazer a requisição à API
        parametros = {
            'dataInicial': data_inicio_formatted,
            'dataFinal': data_fim_formatted,
            'cnpjOrgao': cnpj_clean,
            'pagina': 1,
            'tamanhoPagina': 10
        }

        try:
            response = requests.get(url, params=parametros)
            if response.status_code == 200:
                data = response.json()
                contratos = processamento_dos_dados(data)
                return Response({
                    'orgao': contratos[0].orgao.nome,
                    'cnpj': contratos[0].orgao.cnpj,
                    'contratos': [contrato.objeto for contrato in contratos],
                    'valor_total': sum(contrato.valor_inicial for contrato in contratos)
                })
            else:
                return Response({"error": "Erro ao buscar dados da API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Erro ao buscar dados: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home(request):
    """
    Função responsável por lidar com a página inicial de consultas de contratos.

    Esta função processa as requisições POST enviadas pelo formulário da página inicial para buscar
    informações de contratos de um determinado órgão público, com base no CNPJ e no intervalo de datas fornecido.

    A função realiza as seguintes etapas:
    1. Captura os dados do formulário via POST, incluindo as datas de início e fim, e o CNPJ do órgão.
    2. Formata as datas para o padrão 'yyyyMMdd' para compatibilidade com a API.
    3. Verifica se já existem contratos no banco de dados que correspondem ao CNPJ e ao período fornecido.
        - Se contratos forem encontrados, renderiza a página com esses dados.
        - Se não forem encontrados, faz uma requisição à API pública para obter os contratos.
    4. Caso a API retorne dados válidos, processa e armazena esses contratos no banco de dados,
       e em seguida, renderiza a página com os contratos recém-obtidos.
    5. Em caso de erro, renderiza a página com uma mensagem de erro adequada.

    Parâmetros:
    request (HttpRequest): O objeto da requisição HTTP contendo os dados enviados pelo formulário.

    Retornos:
    HttpResponse: Retorna a página 'index.html' renderizada com os dados do órgão e dos contratos
                  ou com uma mensagem de erro, dependendo do resultado do processamento.
    """
    url = "https://pncp.gov.br/api/consulta/v1/contratos"
    
    if request.method == 'POST':
        data_inicio = request.POST.get('datainicio')
        data_fim = request.POST.get('datafim')
        cnpj = request.POST.get('cnpj')
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))

        # Converter as datas para 'yyyyMMdd'
        try:
            data_inicio_formatted = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%Y%m%d')
            data_fim_formatted = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%Y%m%d')
        except ValueError:
            return render(request, 'index.html', {'error': 'Formato de data inválido.'})
        
        # Verificar se já existem contratos no banco de dados para o CNPJ e período especificado
        contratos_existentes = Contrato.objects.filter(orgao__cnpj=cnpj_clean, 
                                                       data_vigencia_inicial__gte=data_inicio, 
                                                       data_vigencia_final__lte=data_fim)

        if contratos_existentes.exists():
            orgao = contratos_existentes.first().orgao
            valor_total_contratos = sum(contrato.valor_inicial for contrato in contratos_existentes)
            return render(request, 'index.html', {
                'orgao': orgao,
                'contratos': contratos_existentes,
                'valor_total': valor_total_contratos,
                'scroll_to': 'dados-contratos' 
            })

        # Se não há dados no banco, fazer a requisição à API
        parametros = {
            'dataInicial': data_inicio_formatted,
            'dataFinal': data_fim_formatted,
            'cnpjOrgao': cnpj_clean,
            'pagina': 1,
            'tamanhoPagina': 10 
        }
        
        try:
            response = requests.get(url, params=parametros)
            if response.status_code == 200:
                data = response.json()
                contratos = processamento_dos_dados(data)
                if contratos:
                    return render(request, 'index.html', {
                        'orgao': contratos[0].orgao,
                        'contratos': contratos,
                        'valor_total': sum(contrato.valor_inicial for contrato in contratos),
                        'erro_sucess': 'Dados processados com sucesso.',
                        'scroll_to': '#dados-contratos' 
                    })
                    
                else:
                    return render(request, 'index.html', {'erro_sucess': 'Nenhum contrato encontrado.'})
            else:
                return render(request, 'index.html', {'erro_sucess': 'Erro ao buscar dados da API.'})
        except Exception as e:
            return render(request, 'index.html', {'erro_sucess': f'Erro ao buscar dados: {str(e)}'})
    return render(request, 'index.html')


def processamento_dos_dados(data):
    """
    Processa os dados recebidos da API e retorna uma lista de contratos processados.

    Esta função realiza as seguintes operações:
    1. Itera sobre os contratos retornados pela API.
    2. Verifica a existência do órgão relacionado ao contrato no banco de dados:
       - Se o órgão já existir, ele será utilizado.
       - Se o órgão não existir, ele será criado.
    3. Extrai informações relevantes de cada contrato, como:
       - Data de vigência inicial e final.
       - Nome do fornecedor.
       - Objeto do contrato.
       - Valor inicial do contrato.
    4. Cria registros de contratos no banco de dados com as informações extraídas.
    5. Soma os valores iniciais dos contratos para calcular o valor total.
    
    Parâmetros:
    data (dict): Dados recebidos da API, contendo informações sobre contratos e órgãos.

    Retornos:
    tuple: Retorna uma tupla contendo o órgão (Orgao) e o valor total dos contratos processados (float).
    """
    valor_total_contratos = 0
    orgao = None

    # Processar os contratos encontrados
    for contrato in data.get('data', []):
        orgao_info = contrato.get('orgaoEntidade', None)

        if not orgao_info:
            continue

        cnpj_orgao = orgao_info.get('cnpj')
        nome_orgao = orgao_info.get('razaoSocial')

        orgao, created = Orgao.objects.get_or_create(cnpj=cnpj_orgao, defaults={'nome': nome_orgao})

        data_vigencia_inicial = contrato.get('dataVigenciaInicio')
        data_vigencia_final = contrato.get('dataVigenciaFim')
        razao_social_fornecedor = contrato.get('nomeRazaoSocialFornecedor')
        objeto_contrato = contrato.get('objetoContrato')
        valor_inicial = contrato.get('valorInicial', 0)

        Contrato.objects.create(
            orgao=orgao,
            data_vigencia_inicial=data_vigencia_inicial,
            data_vigencia_final=data_vigencia_final,
            razao_social_fornecedor=razao_social_fornecedor,
            objeto=objeto_contrato,
            valor_inicial=valor_inicial
        )

        valor_total_contratos += valor_inicial

    return orgao, valor_total_contratos



