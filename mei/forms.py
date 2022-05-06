from django.forms import ModelForm, TextInput, Textarea, FileInput, NumberInput, DateInput

from mei.models import DespesaComprovada


class DespesaComprovadaForm(ModelForm):
    class Meta:
        model = DespesaComprovada
        fields = ('nome', 'descricao', 'valor', 'arquivo', 'data_pagamento')
        labels = {
            'nome': 'Nome arquivo',
            'descricao': 'Descrição',
            'valor': 'Valor',
            'arquivo': 'Arquivo',
            'data_pagamento': 'Data de pagamento'
        }
        widgets = {
            'nome': TextInput(attrs={'class': "form-control"}),
            'descricao': Textarea(attrs={'class': "form-control", 'style': "height: 100px"}),
            'valor': NumberInput(attrs={'class': "form-control"}),
            'arquivo': FileInput(attrs={'class': "form-control"}),
            'data_pagamento': DateInput(attrs={'class': "form-control"})
        }
