import xml.etree.ElementTree as ET
from datetime import datetime

from faturamento.models import NFE, Servico
from clientes.models import Cliente, Endereco


class LoadXML():

    def __init__(self, xml):
        self.xml = xml

    def nef_ginfes_maceio(self):
        nsNfe = {
            "ns2": "http://www.w3.org/2000/09/xmldsig#",
            "ns3": "http://www.ginfes.com.br/tipos",
            "ns4": "http://www.ginfes.com.br/servico_consultar_nfse_envio",
            "ns5": "http://www.ginfes.com.br/servico_cancelar_nfse_envio"
        }
        tree = ET.parse(self.xml)
        root = tree.getroot()
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
                CNPJ=self.format_cnpj(nfe.find('ns3:TomadorServico/ns3:IdentificacaoTomador/ns3:CpfCnpj/ns3:Cnpj', nsNfe)),
                razao_social=self.nao_esta_nulo(nfe.find('ns3:TomadorServico/ns3:RazaoSocial', nsNfe)),
                endereco=endereco
            )

            servico = Servico(
                valor_servicos=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorServicos', nsNfe))),
                iss_retido=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:IssRetido', nsNfe))),
                valor_iss=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorIss', nsNfe))),
                base_calculo=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:BaseCalculo', nsNfe))),
                aliquota=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:Aliquota', nsNfe))),
                valor_liquido_nfse=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorLiquidoNfse', nsNfe))),
                valor_iss_retido=float(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Valores/ns3:ValorIssRetido', nsNfe))),
                item_lista_servico=int(self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:ItemListaServico', nsNfe))),
                codigo_tributacao_municipio=self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:CodigoTributacaoMunicipio', nsNfe)),
                descricao=self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:Discriminacao', nsNfe)),
                municipio_prestacao_servico=self.nao_esta_nulo(nfe.find('ns3:Servico/ns3:MunicipioPrestacaoServico', nsNfe)),
            )

            nfe = NFE(
                numero=int(self.nao_esta_nulo(nfe.find('ns3:IdentificacaoNfse/ns3:Numero', nsNfe))),
                codigo_verificacao=self.nao_esta_nulo(nfe.find('ns3:IdentificacaoNfse/ns3:CodigoVerificacao', nsNfe)),
                data_emissao=self.format_data(self.nao_esta_nulo(nfe.find('ns3:DataEmissao', nsNfe))),
                natureza_operacao=int(self.nao_esta_nulo(nfe.find('ns3:NaturezaOperacao', nsNfe))),
                regime_especial_tributacao=int(self.nao_esta_nulo(nfe.find('ns3:RegimeEspecialTributacao', nsNfe))),
                optante_simples_nacional=int(self.nao_esta_nulo(nfe.find('ns3:OptanteSimplesNacional', nsNfe))),
                incetivador_cultural=int(self.nao_esta_nulo(nfe.find('ns3:IncetivadorCultural', nsNfe))),
                competencia=self.nao_esta_nulo(nfe.find('ns3:Competencia', nsNfe)),
                tomador=cliente,
                servico=servico
            )
            # print("==========================")
            # print(nfe)
            # print("==========================")


            nfes.append(nfe)
        return nfes

    def format_cnpj(self, cnpj_t):
        try:
            cnpj = cnpj_t.text
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
        except:
            return ""

    def format_data(self, data):
        return datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')

    def nao_esta_nulo(self, object):
        if object is not None:
            return object.text
        else:
            return ""