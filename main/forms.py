from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Gol, Pagamento, User, Partida
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(forms.Form):
    nome_jogador = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Senha')

class ChangePasswordForm(PasswordChangeForm):
    nova_senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_nova_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['senha_atual', 'nova_senha', 'confirmar_nova_senha']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'nome_completo',
            'nome_jogador',
            'posicao',
            'email',
            'telefone',
            'time_coracao',
            'data_nascimento',
            'uf_nascimento',
            'cidade_nascimento',
            'altura',
        )
        
        labels = {
            'nome_jogador': 'Nome de Jogador',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'altura': 'Altura',
            'nome_completo': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'uf_nascimento': 'UF de Nascimento',
            'cidade_nascimento': 'Cidade de Nascimento',
            'posicao': 'Posição',
            'time_coracao': 'Time do Coração',
        }

        widgets = {
            'nome_jogador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'uf_nascimento': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'cidade_nascimento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'posicao': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'time_coracao': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
        }
        required = {
            'nome_jogador': True,
            'email': False,
            'telefone': False,
            'altura': False,
            'nome_completo': False,
            'data_nascimento': False,
            'uf_nascimento': False,
            'cidade_nascimento': False,
            'posicao': True,
            'time_coracao': False,
        }

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('nome_jogador', 'posicao')

        labels = {
            'nome_jogador': 'Nome de Jogador',
            'posicao': 'Posição',
        }

        widgets = {
            'nome_jogador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'posicao': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
        }


class PartidaForm(forms.Form):

    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label=_('Data'))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), label=_('Hora'))
    
    class Meta:
        model = Partida
        fields = ['data', 'hora']

class PagamentoForm(forms.ModelForm):
    comprovante = forms.ImageField(widget=forms.FileInput(attrs={'id': 'comprovante', 'class': 'form-control'}), label=_('Envie o comprovante aqui:'), required=False)
    em_dinheiro = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        required=False,
        label='Pagamento em dinheiro?'
    )
    valor = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label=_('Qual o valor?'), required=True)

    
    class Meta:
        model = Pagamento
        fields = ['comprovante', 'em_dinheiro', 'valor']


class AdicionarConvidadoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nome_jogador', 'posicao')
        labels = {
            'nome_jogador': 'Nome de Jogador',
            'posicao': 'Posição',
        }
        widgets = {
            'nome_jogador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'posicao': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
        }
        
class AdicionarConvidadoExistenteForm(forms.Form):
    
    convidado = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-select'}),label='Adicione um convidado', queryset=User.objects.filter(tipo='convidado'), required=False)
    
    class Meta:
        model = User

from django import forms

class GolForm(forms.ModelForm):
    class Meta:
        model = Gol
        fields = ['jogador', 'quantidade']
        widgets = {
            'jogador': forms.Select(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'dummy'}),
        }
