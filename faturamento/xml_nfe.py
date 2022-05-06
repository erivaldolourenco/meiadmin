import xml.etree.ElementTree as ET
from datetime import datetime

from faturamento.models import NFE, Servico
from clientes.models import Cliente, Endereco
from django.contrib import messages

class LoadXML():

    def __init__(self, xml, request):
        self.xml = xml
        self.request = request

    def obter_nfes(self):
        tree = ET.parse(self.xml)
        root = tree.getroot()
        print(root.tag)
        if '{http://www.w3.org/2000/09/xmldsig#}NFSE' in root.tag:
            return self.nfe_ginfes_maceio(root)
        if '{http://www.giss.com.br/tipos-v2_04.xsd}CompNfse' in root.tag:
            print('NFE GISS')
            return self.nfe_giss_maceio(root)
        else:
            print('Sem xml')
            return None

    def nfe_giss_maceio(self, root):
        nsNfe = {
            "ns2": "http://www.giss.com.br/tipos-v2_04.xsd",
            "ns3": "http://www.w3.org/2000/09/xmldsig#",
        }

        nfes = []
        for nfe in root.findall('ns2:Nfse/ns2:InfNfse', nsNfe):
            endereco_path = 'ns2:DeclaracaoPrestacaoServico/ns2:InfDeclaracaoPrestacaoServico/ns2:TomadorServico/ns2:Endereco/'
            endereco = Endereco(
                endereco=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Endereco', nsNfe)),
                numero=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Numero', nsNfe)),
                complemento=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Complemento', nsNfe)),
                bairro=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Bairro', nsNfe)),
                cidade=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:CodigoMunicipio', nsNfe)),
                estado=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Uf', nsNfe)),
                cep=self.nao_esta_nulo(nfe.find(endereco_path+'ns2:Cep', nsNfe)),
            )

            cliente_path = 'ns2:DeclaracaoPrestacaoServico/ns2:InfDeclaracaoPrestacaoServico/ns2:TomadorServico/'
            cliente = Cliente(
                cnpj=self.nao_esta_nulo(
                    nfe.find(cliente_path+'ns2:IdentificacaoTomador/ns2:CpfCnpj/ns2:Cnpj', nsNfe)),
                razao_social=self.nao_esta_nulo(nfe.find(cliente_path+'ns2:RazaoSocial', nsNfe)),
                endereco=endereco
            )
            cliente.mei = self.request.user.responsavel.mei
            cliente = self.salvar_cliente(cliente)

            servico_path = 'ns2:DeclaracaoPrestacaoServico/ns2:InfDeclaracaoPrestacaoServico/ns2:Servico/'
            servico = Servico(
                valor_servicos=float(self.nao_esta_nulo(nfe.find(servico_path+'ns2:Valores/ns2:ValorServicos', nsNfe))),
                iss_retido=float(self.nao_esta_nulo(nfe.find(servico_path+'ns2:IssRetido', nsNfe))),
                valor_iss=float(self.nao_esta_nulo(nfe.find(servico_path+'ns2:Valores/ns2:ValorIss', nsNfe))),
                base_calculo=float(self.nao_esta_nulo(nfe.find('ns2:ValoresNfse/ns2:BaseCalculo', nsNfe))),
                aliquota=float(self.nao_esta_nulo(nfe.find(servico_path+'ns2:Valores/ns2:Aliquota', nsNfe))),
                valor_liquido_nfse=float(
                    self.nao_esta_nulo(nfe.find('ns2:ValoresNfse/ns2:ValorLiquidoNfse', nsNfe))),
                valor_iss_retido=float(
                    self.nao_esta_nulo(nfe.find(servico_path+'ns2:Valores/ns2:ValorIss', nsNfe))),
                item_lista_servico=self.nao_esta_nulo(nfe.find(servico_path+'ns2:ItemListaServico', nsNfe)),
                codigo_tributacao_municipio=self.nao_esta_nulo(
                    nfe.find(servico_path+'ns2:CodigoTributacaoMunicipio', nsNfe)),
                descricao=self.nao_esta_nulo(nfe.find(servico_path+'ns2:Discriminacao', nsNfe)),
                municipio_prestacao_servico=self.nao_esta_nulo(
                    nfe.find(servico_path+'ns2:CodigoMunicipio', nsNfe)),
            )

            nfe_path = 'ns2:DeclaracaoPrestacaoServico/ns2:InfDeclaracaoPrestacaoServico/'

            print("-------------------------")
            print(nfe.find(nfe_path+'ns2:RegimeEspecialTributacao', nsNfe).text)
            print("-------------------------")

            mei = self.request.user.responsavel.mei

            nfe = NFE(
                numero=int(self.nao_esta_nulo(nfe.find('ns2:Numero', nsNfe))),
                codigo_verificacao=self.nao_esta_nulo(nfe.find('ns2:CodigoVerificacao', nsNfe)),
                data_emissao=self.format_data2(self.nao_esta_nulo(nfe.find('ns2:DataEmissao', nsNfe))),
                natureza_operacao=self.nao_esta_nulo(nfe.find('ns2:DescricaoCodigoTributacaoMunicipio', nsNfe)),
                regime_especial_tributacao=int(self.nao_esta_nulo(nfe.find(nfe_path+'ns2:RegimeEspecialTributacao', nsNfe))),
                optante_simples_nacional=int(self.nao_esta_nulo(nfe.find(nfe_path+'ns2:OptanteSimplesNacional', nsNfe))),
                incetivador_cultural=int(self.nao_esta_nulo(nfe.find(nfe_path+'ns2:IncentivoFiscal', nsNfe))),
                competencia=self.nao_esta_nulo(nfe.find(nfe_path+'ns2:Competencia', nsNfe)),
                cliente=cliente,
                servico=servico,
                mei = mei
            )
            self.salvar_nfe(nfe)
            print("==========================")
            print(nfe)
            print("==========================")

            nfes.append(nfe)

        return nfes



    def nfe_ginfes_maceio(self, root):
        nsNfe = {
            "ns2": "http://www.w3.org/2000/09/xmldsig#",
            "ns3": "http://www.ginfes.com.br/tipos",
            "ns4": "http://www.ginfes.com.br/servico_consultar_nfse_envio",
            "ns5": "http://www.ginfes.com.br/servico_cancelar_nfse_envio"
        }
        nfes = []
        for nfe in root.findall('ns2:Nfse', nsNfe):
            endereco = Endereco(
                endereco=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Endereco', nsNfe)),
                numero=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Numero', nsNfe)),
                complemento=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Complemento', nsNfe)),
                bairro=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Bairro', nsNfe)),
                cidade=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Cidade', nsNfe)),
                estado=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Estado', nsNfe)),
                cep=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:Endereco/ns3:Cep', nsNfe)),
            )

            # print(nfe.find('ns3:TomadorServico/ns3:IdentificacaoTomador/ns3:CpfCnpj/ns3:Cnpj', nsNfe).text)
            cliente = Cliente(
                cnpj=self.nao_esta_nulo(
                    nfe.find('ns3:TomadorServico/ns3:IdentificacaoTomador/ns3:CpfCnpj/ns3:Cnpj', nsNfe)),
                razao_social=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:RazaoSocial', nsNfe)),
                endereco=endereco
            )
            cliente.mei = self.request.user.responsavel.mei
            cliente = self.salvar_cliente(cliente)

            servico = Servico(
                valor_servicos=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorServicos', nsNfe))),
                iss_retido=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:IssRetido', nsNfe))),
                valor_iss=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorIss', nsNfe))),
                base_calculo=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:BaseCalculo', nsNfe))),
                aliquota=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:Aliquota', nsNfe))),
                valor_liquido_nfse=float(
                    self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorLiquidoNfse', nsNfe))),
                valor_iss_retido=float(
                    self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorIssRetido', nsNfe))),
                item_lista_servico=self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:ItemListaServico', nsNfe)),
                codigo_tributacao_municipio=self.nao_esta_nulo(
                    nfe.find('ns3:Servico/ns3:CodigoTributacaoMunicipio', nsNfe)),
                descricao=self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Discriminacao', nsNfe)),
                municipio_prestacao_servico=self.nao_esta_nulo(
                    nfe.find('ns3:Servico/ns3:MunicipioPrestacaoServico', nsNfe)),
            )
            mei =  self.request.user.responsavel.mei
            nfe = NFE(
                numero=int(self.nao_esta_nulo(nfe.find('ns3:IdentificacaoNfse/ns3:Numero', nsNfe))),
                codigo_verificacao=self.nao_esta_nulo(nfe.find('ns3:IdentificacaoNfse/ns3:CodigoVerificacao', nsNfe)),
                data_emissao=self.format_data(self.nao_esta_nulo(nfe.find('ns3:DataEmissao', nsNfe))),
                natureza_operacao=self.nao_esta_nulo(nfe.find('ns3:NaturezaOperacao', nsNfe)),
                regime_especial_tributacao=int(self.nao_esta_nulo(nfe.find('ns3:RegimeEspecialTributacao', nsNfe))),
                optante_simples_nacional=int(self.nao_esta_nulo(nfe.find('ns3:OptanteSimplesNacional', nsNfe))),
                incetivador_cultural=int(self.nao_esta_nulo(nfe.find('ns3:IncetivadorCultural', nsNfe))),
                competencia=self.nao_esta_nulo(nfe.find('ns3:Competencia', nsNfe)),
                cliente=cliente,
                servico=servico,
                mei=mei
            )
            self.salvar_nfe(nfe)
            # print("==========================")
            # print(nfe)
            # print("==========================")

            nfes.append(nfe)
        return nfes

    def format_data(self, data):
        return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    
    def format_data2(self, data):
        return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f%z')

    def nao_esta_nulo(self, object):
        if object is not None:
            return object.text
        else:
            return ""

    def salvar_cliente(self, cliente):
        try:
            return Cliente.objects.get(cnpj=cliente.cnpj)
        except:
            cliente.endereco.save()
            cliente.save()
            return Cliente.objects.get(id=cliente.id)


    def salvar_nfe(self, nfe):
        try:
            nfe = NFE.objects.get(numero=nfe.numero)
            messages.add_message(
                self.request, messages.INFO,
                'Nota fiscal '+str(nfe.numero)+' já existe!',
                fail_silently=True,
            )
            return nfe
        except NFE.DoesNotExist:
            nfe.servico.save()
            nfe.save()
            return nfe
        else:
            return  nfe.servico.delete()

