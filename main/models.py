from collections import defaultdict
from django.db import models
from financeiro.models import Saida

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum

from datetime import date
from uuid import uuid4


class Configuracao(models.Model):

    ALERTA_CORES = (
        ('warning', 'Amarelo'),
        ('danger', 'Vermelho'),
        ('success', 'Verde'), 
        ('dark', 'Preto'),
        ('primary', 'Azul'),
        ('info', 'Azul-Claro'),
        ('secondary', 'Cinza'),
        ('light', 'Branco')
    )
    
    ALERTA_ICONES = (
        ('#exclamation-triangle-fill', 'Triângulo com Exclamação'),
        ('#info-fill', 'Círculo com "i"'),
        ('#check-circle-fill', 'Círculo com "check"')
    )

    # Do Diretor
    telefone_diretor = models.CharField(_('Telefone do Diretor:'), max_length=100)
    email_diretor = models.EmailField(_('E-mail do Diretor:'))
    # Do Pagamento
    qr_code_pagamento = models.ImageField(_('QR Para pagamentos:'), upload_to='main/images/')
    chave_pix = models.CharField(_('Chave pix para pagamentos:'), max_length=50, blank=True, null=True)
    # Do Site
    regras_federacao = models.TextField(_('Regras da Federação:'))
    alerta_mensagem = models.CharField(_('Mensagem do Alerta:'), max_length=100, blank=True, null=True)
    alerta_link = models.URLField(_('Link do Alerta:'), max_length=200, blank=True, null=True)
    alerta_texto_link = models.CharField(_('Texto do link do Alerta:'), max_length=50, blank=True, null=True)
    alerta_cor = models.CharField(_('Cor do Alerta:'), default='warning', max_length=50, choices=ALERTA_CORES, blank=True, null=True)
    alerta_icon = models.CharField(_('Ícone do Alerta:'), default=None, max_length=50, choices=ALERTA_ICONES, blank=True, null=True)
    
    # Do Financeiro
    @property
    def saldo(self):
        pagamentos_confirmados = Pagamento.objects.filter(confirmado=True).aggregate(total=Sum('valor'))['total']
        saidas_total = Saida.objects.aggregate(total=Sum('valor'))['total']
        saldo = pagamentos_confirmados - saidas_total if pagamentos_confirmados is not None and saidas_total is not None else '[ERRO!]'
        return saldo
    
    # Metadados
    def __str__(self):
        return 'Configurações'
    
    class Meta:
        verbose_name = 'Configurações'
        verbose_name_plural = 'Configurações'
        
    # Restrição para um só objeto
    def save(self, *args, **kwargs):
        if not self.pk and Configuracao.objects.exists():
            return Configuracao.objects.first()
        return super().save(*args, **kwargs)

class Administrador(BaseUserManager):
    def _create_user(self, nome_jogador, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not nome_jogador:
            raise ValueError(_('O nome de jogador deve ser definido!'))
        user = self.model(nome_jogador=nome_jogador, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, nome_jogador=None, password=None, **extra_fields):
        return self._create_user(nome_jogador, password, False, False, **extra_fields)
    def create_superuser(self, nome_jogador, password, **extra_fields):
        user=self._create_user(nome_jogador, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    TIPO = (
        ('admin', 'Administrador'),
        ('federado', 'Federado'),
        ('convidado', 'Convidado'),
    )  

    POSICOES = (
        ('goleiro', 'Goleiro'),
        ('zagueiro', 'Zagueiro'),
        ('lateral', 'Lateral'),
        ('volante', 'Volante'),
        ('meia', 'Meia'),
        ('ponta', 'Ponta'),
        ('centroavante', 'Centroavante'),
    )

    TIMES = (
        ('gremio', 'Grêmio'),
        ('santos', 'Santos'),
        ('cruzeiro', 'Cruzeiro'),
        ('palmeiras', 'Palmeiras'),
        ('atletico_mineiro', 'Atlético Mineiro'),
        ('botafogo', 'Botafogo'),
        ('flamengo', 'Flamengo'),
        ('fluminense', 'Fluminense'),
        ('internacional', 'Internacional'),
        ('sao_paulo', 'São Paulo'),
        ('vasco_da_gama', 'Vasco da Gama'),
        ('corinthians', 'Corinthians'),
        ('bahia', 'Bahia'),
        ('athletico_paranaense', 'Athletico Paranaense'),
        ('sport', 'Sport'),
        ('goias', 'Goiás'),
        ('coritiba', 'Coritiba'),
        ('vitoria', 'Vitória'),
        ('portuguesa', 'Portuguesa'),
        ('nautico', 'Náutico'),
        ('guarani', 'Guarani'),
        ('paysandu', 'Paysandu'),
        ('ceara', 'Ceará'),
        ('santa_cruz', 'Santa Cruz'),
        ('ponte_preta', 'Ponte Preta'),
        ('fortaleza', 'Fortaleza'),
        ('csa', 'CSA'),
        ('america_rj', 'America-RJ'),
        ('america_mineiro', 'América Mineiro'),
        ('figueirense', 'Figueirense'),
        ('juventude', 'Juventude'),
        ('remo', 'Remo'),
        ('parana', 'Paraná'),
        ('nacional_am', 'Nacional-AM'),
        ('america_rn', 'América-RN'),
        ('desportiva_ferroviaria', 'Desportiva Ferroviária-ES'),
        ('abc', 'ABC'),
        ('criciuma', 'Criciúma'),
        ('joinville', 'Joinville'),
        ('sampaio_correa', 'Sampaio Corrêa'),
        ('atletico_goianiense', 'Atlético Goianiense'),
        ('sergipe', 'Sergipe'),
        ('rio_branco_es', 'Rio Branco-ES'),
        ('crb', 'CRB'),
        ('bragantino', 'Bragantino'),
        ('moto_club', 'Moto Club'),
        ('bangu', 'Bangu'),
        ('campinense', 'Campinense'),
        ('avai', 'Avaí'),
        ('operario_ms', 'Operário-MS'),
        ('vila_nova', 'Vila Nova'),
        ('treze', 'Treze'),
        ('chapecoense', 'Chapecoense'),
        ('americano_rj', 'Americano-RJ'),
        ('confianca', 'Confiança'),
        ('river_pi', 'River-PI'),
        ('mixto_mt', 'Mixto-MT'),
        ('londrina', 'Londrina'),
        ('sao_caetano_sp', 'São Caetano-SP'),
        ('rio_negro_am', 'Rio Negro-AM'),
        ('botafogo_pb', 'Botafogo-PB'),
        ('flamengo_pi', 'Flamengo-PI'),
        ('inter_de_limeira', 'Inter de Limeira'),
        ('brasilia', 'Brasília'),
        ('botafogo_sp', 'Botafogo-SP'),
        ('gama', 'Gama'),
        ('ferroviario_ce', 'Ferroviário-CE'),
        ('gremio_maringa', 'Grêmio Maringá'),
        ('uberaba_mg', 'Uberaba-MG'),
        ('goytacaz_rj', 'Goytacaz-RJ'),
        ('comercial_ms', 'Comercial-MS'),
        ('itabaiana_se', 'Itabaiana-SE'),
        ('tiradentes_pi', 'Tiradentes-PI'),
        ('tuna_luso', 'Tuna Luso'),
        ('anapolina', 'Anapolina'),
        ('caxias_do_sul', 'Caxias do Sul'),
        ('brasil_de_pelotas', 'Brasil de Pelotas'),
        ('uniao_sao_joao_sp', 'União São João-SP'),
        ('uberlandia', 'Uberlândia'),
        ('fluminense_de_feira', 'Fluminense de Feira'),
        ('ceov_mt', 'CEOV-MT'),
        ('goiania', 'Goiânia'),
        ('piaui', 'Piauí'),
        ('xv_de_piracicaba', 'XV de Piracicaba'),
        ('volta_redonda', 'Volta Redonda'),
        ('maranhao', 'Maranhão'),
        ('leonico_ba', 'Leônico-BA'),
        ('villa_nova_mg', 'Villa Nova-MG'),
        ('fast_clube_am', 'Fast Clube-AM'),
        ('alecrim_rn', 'Alecrim-RN'),
        ('sao_paulo_rs', 'São Paulo-RS'),
        ('dom_bosco_mt', 'Dom Bosco-MT'),
        ('ceub_df', 'CEUB-DF'),
        ('ferroviario_pr', 'Ferroviário-PR'),
        ('fonseca_rj', 'Fonseca-RJ'),
        ('rabello_df', 'Rabello-DF'),
        ('central_pe', 'Central-PE'),
        ('santo_andre', 'Santo André'),
        ('america_sp', 'América-SP'),
        ('campo_grande_rj', 'Campo Grande-RJ'),
        ('gremio_barueri', 'Grêmio Barueri'),
        ('pinheiros_pr', 'Pinheiros-PR'),
        ('sao_jose_sp', 'São José-SP'),
        ('itabuna_ba', 'Itabuna-BA'),
        ('comercial_sp', 'Comercial-SP'),
        ('glicia_ba', 'Galícia-BA'),
        ('capelense_al', 'Capelense-AL'),
        ('olaria_rj', 'Olaria-RJ'),
        ('xv_de_jau', 'XV de Jaú'),
        ('santa_cruz_se', 'Santa Cruz-SE'),
        ('santo_antonio_es', 'Santo Antônio - ES'),
        ('juventus_sp', 'Juventus-SP'),
        ('catuense_ba', 'Catuense-BA'),
        ('nova_hamburgo_rs', 'Nova Hamburgo-RS'),
        ('asa_de_arapiraca', 'ASA de Arapiraca'),
        ('brasiliense', 'Brasiliense'),
        ('operario_pr', 'Operário-PR'),
        ('itumbiara_go', 'Itumbiara-GO'),
        ('taguatinga_df', 'Taguatinga-DF'),
        ('ipatinga_mg', 'Ipatinga-MG'),
        ('noroeste_sp', 'Noroeste-SP'),
        ('sao_bento_sp', 'São Bento-SP'),
        ('anapolis_go', 'Anápolis-GO'),
        ('vitoria_es', 'Vitória-ES'),
        ('ferroviaria_sp', 'Ferroviária-SP'),
        ('colatina_es', 'Colatina-ES'),
        ('guara_df', 'Guará-DF'),
        ('sobradinho_df', 'Sobradinho-DF'),
        ('cuiaba_mt', 'Cuiabá-MT'),
        ('inter_de_santa_maria_rs', 'Inter de Santa Maria-RS'),
        ('auto_esporte_pb', 'Auto Esporte-PB'),
        ('j_malucelli_pr', 'J. Malucelli-PR'),
        ('caldense', 'Caldense'),
        ('corumbaense', 'Corumbaense'),
        ('auto_esporte_pi', 'Auto Esporte-PI'),
        ('ferroviario_ma', 'Ferroviário-MA'),
        ('potiguar_de_mossoro_rn', 'Potiguar de Mossoró-RN'),
        ('francana_sp', 'Francana-SP'),
        ('america_de_propria_se', 'América de Própria-SE'),
        ('rio_branco_rj', 'Rio Branco-RJ'),
        ('inter_de_lages_sc', 'Inter de Lages-SC'),
        ('hercilio_luz_sc', 'Hercílio Luz-SC'),
        ('agua_verde_pr', 'Agua Verde-PR'),
        ('america_ce', 'América-CE'),
        ('comercial_pr', 'Comercial-PR'),
        ('defele_df', 'Defelê-DF'),
        ('cruzeiro_do_sul_df', 'Cruzeiro do Sul-DF'),
        ('eletrovapo_rj', 'Eletrovapo-RJ'),
        ('estrela_do_mar_pb', 'Estrela do Mar-PB'),
        ('guanabara_df', 'Guanabara-DF'),
        ('manufatora_rj', 'Manufatora-RJ'),
        ('olimpico_am', 'Olímpico-AM'),
        ('olimpico_sc', 'Olímpico - SC'),
        ('paula_ramos_sc', 'Paula Ramos-SC'),
        ('perdigao_sc', 'Perdigão-SC'),
        ('siderurgica_mg', 'Siderúrgica-MG')
    )

    UF_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    senha_validator = RegexValidator(
        regex=r'^(?=.*[\W_])(?=.*[A-Z]).{8,}$',
        message="A senha deve conter no mínimo um caractere especial ou um caractere maiúsculo e ter pelo menos 8 caracteres."
    )
    
    telefone_validator = RegexValidator(
        regex=r'^[0-9\- ]*$',
        message="O telefone deve conter apenas números, hífens (-) e espaços."
    )
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    # Informações de Login
    nome_jogador = models.CharField(_('Nome de Jogador:'), default='', max_length=50, unique=True)
    is_staff = models.BooleanField(_('É administrador?'), default=False, help_text=_('Isso define se o usuário tem ou não acesso à esta administração do site.'))
    is_active = models.BooleanField(_('Está ativo?'), default=True, help_text=_('Isso defino se o usuário é ativo no sistema.'))
    date_joined = models.DateTimeField(_('Data de Registro:'), default=timezone.now)
    tipo = models.CharField(_('Tipo:'), default='federado', max_length=50, choices=TIPO)
    # Informações de Contato
    email = models.EmailField(_('E-mail:'), max_length=254, null=True, blank=True)
    telefone = models.CharField(_('Telefone:'), max_length=20, validators=[telefone_validator], null=True, blank=True)
    # Informações Físicas
    foto_principal = models.ImageField(_('Foto principal:'), upload_to='main/foto_jogador', null=True, blank=True)
    foto_secundaria = models.ImageField(_('Foto com colete:'), upload_to='main/foto_jogador', null=True, blank=True)
    altura = models.DecimalField(_('Altura:'), max_digits=3, decimal_places=2, null=True, blank=True)
    # Informações de Nascimento
    nome_completo = models.CharField(_('Nome completo:'), max_length=100, null=True, blank=True)
    data_nascimento = models.DateField(_('Data de nascimento:'), null=True, blank=True)
    uf_nascimento = models.CharField(_('Estado natal:'), max_length=20, choices=UF_CHOICES, null=True, blank=True)
    cidade_nascimento = models.CharField(_('Cidade natal:'), max_length=50, null=True, blank=True)
    # Informações de Futebol
    posicao = models.CharField(_('Posição:'), max_length=50, choices=POSICOES)
    time_coracao = models.CharField(_('Time do Coração:'), max_length=50, choices=TIMES, null=True, blank=True)
    gols_marcados = models.PositiveSmallIntegerField(_('Gols marcados:'), default=0, null=True, blank=True)
    pontos = models.SmallIntegerField(_('Pontos:'), default=0, null=True, blank=True)

    slug = models.SlugField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome_jogador)
        super().save(*args, **kwargs)
    
    @property
    def idade(self):
        if self.data_nascimento is None:
            return 'Infome sua data de nascimento'

        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year

        if hoje.month < self.data_nascimento.month or (hoje.month == self.data_nascimento.month and hoje.day < self.data_nascimento.day):
            idade -= 1

        return idade
    
    @property
    def partidas_jogadas(self):
        
        usuario = self
        
        partidas_time_verde = Partida.objects.filter(time_verde=usuario)
        total_partidas_time_verde = partidas_time_verde.count()

        partidas_time_vermelho = Partida.objects.filter(time_vermelho=usuario)
        total_partidas_time_vermelho = partidas_time_vermelho.count()

        partidas_time_azul = Partida.objects.filter(time_azul=usuario)
        total_partidas_time_azul = partidas_time_azul.count()

        partidas_jogadas = total_partidas_time_verde + total_partidas_time_vermelho + total_partidas_time_azul

        return partidas_jogadas

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.nome_jogador

    USERNAME_FIELD = 'nome_jogador'

    objects = Administrador()

        
class Partida(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    data = models.DateField(_('Data:'), auto_now=False, auto_now_add=False, null=True)
    hora = models.TimeField(_('Horário:'), auto_now=False, auto_now_add=False, null=True)
    relacionados = models.ManyToManyField(User, related_name='relacionados', blank=True)
    time_verde = models.ManyToManyField(User, related_name='partidas_timeA', blank=True)
    time_vermelho = models.ManyToManyField(User, related_name='partidas_timeB', blank=True)
    time_azul = models.ManyToManyField(User, related_name='partidas_timeC', blank=True)
    sorteada = models.BooleanField(_('Foi sorteada?'), default=False)
    anulada = models.BooleanField(_('Foi anulada?'), default=False)
    razao_anulacao = models.TextField(_("Qual a razão da anulação?"), blank=True)

    slug = models.SlugField(max_length=50, unique=True, editable=False, default='')
    
    @property
    def cara_da_partida(self):

        votos = self.voto_set.all()
        
        if not votos:
            return None

        contagem_votos = {}

        for voto in votos:
            jogador = voto.votou_em
            if jogador in contagem_votos:
                contagem_votos[jogador] += 1
            else:
                contagem_votos[jogador] = 1

        jogador_mais_votado = max(contagem_votos, key=contagem_votos.get, default=None)

        return jogador_mais_votado
    

    @property
    def artilheiro(self):
        artilheiro_info = (
            Gol.objects
            .filter(partida=self)
            .values('jogador')
            .annotate(total_gols=Sum('quantidade'))
            .order_by('-total_gols')
            .first()
        )
        
        if artilheiro_info:
            jogador_id = artilheiro_info['jogador']
            total_gols_partida = artilheiro_info['total_gols']
            jogador = User.objects.get(id=jogador_id)
            
            todos_gols = (
                Gol.objects
                .filter(jogador=jogador)
                .aggregate(total_gols=Sum('quantidade'))
            )['total_gols']
            
            return jogador, total_gols_partida, todos_gols
        
        return None

    
    def votacao_aberta(self):
        hoje = timezone.now().date()
        data_limite = self.data + timezone.timedelta(days=1)
        return hoje <= data_limite

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

    def __str__(self):
        formatted_data = self.data.strftime("%d/%m/%Y") if self.data else "N/A"
        formatted_hora = self.hora.strftime("%H:%M") if self.hora else "N/A"
        return f"Partida em {formatted_data} às {formatted_hora}"
        

class Voto(models.Model):
    
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votos_feitos')
    votou_em = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votos_recebidos')
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Voto")
        verbose_name_plural = _("Votos")

    def __str__(self):
        return f'{self.jogador.nome_jogador} votou em {self.votou_em.nome_jogador}'

    
class Gol(models.Model):
    
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    quantidade = models.PositiveSmallIntegerField("Quantos gols?")

    class Meta:
        verbose_name = _("Gol")
        verbose_name_plural = _("Gols")

    def __str__(self):
        if self.quantidade > 1:
            return f'{self.jogador} fez {str(self.quantidade)} gols na {self.partida}'
        else:
            return f'{self.jogador} fez {str(self.quantidade)} gol na {self.partida}'


class Pagamento(models.Model):

    comprovante = models.ImageField(_('Comprovante:'), upload_to='main/images/pagamentos', blank=True, null=True)
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, blank=True, null=True)
    em_dinheiro = models.BooleanField(_('Pagamento em dinheiro?'), default=False)
    valor = models.DecimalField(_('Valor do pagamento:'), decimal_places=2, max_digits=5, default=10.00)
    confirmado = models.BooleanField(_('Pagamento confirmado?'), default=False)
    data = models.DateField(_("Data do pagamento"), auto_now_add=True, null=True)
    descricao = models.CharField(_("Descrição do Pagamento:"), max_length=255, blank=True, null=True)
    
    def __str__(self):
        if self.jogador is not None:
            return f'Pagamento de {self.jogador.nome_jogador} em {self.data}'
        else:
            return f'Pagamento em {self.data}'

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'


@deconstructible
class MediaTypeUploadTo:
    def __call__(self, instance, filename):
        media_type = self.get_media_type(filename)
        if media_type == 'image':
            return f"main/images/noticias/{filename}"
        elif media_type == 'video':
            return f"main/videos/noticias/{filename}"
        else:
            return f"main/media/{filename}"

    def get_media_type(self, filename):
        extension = filename.split('.')[-1].lower()
        if extension in ['jpg', 'jpeg', 'png', 'gif']:
            return 'image'
        elif extension in ['mp4', 'avi', 'mov', 'm4a']:
            return 'video'
        else:
            return 'other'


def validate_media_file(value):
    extension = value.name.split('.')[-1].lower()
    if extension not in ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'm4a']:
        raise ValidationError("O arquivo deve ser uma imagem (jpg, jpeg, png, gif) ou um vídeo (mp4, avi, mov, m4a).")


class Noticia(models.Model):
    titulo = models.CharField(_('Título:'), max_length=100)
    texto = models.CharField(_('Texto da Notícia:'), max_length=255)
    midia = models.FileField(_('Imagem ou vídeo:'), upload_to=MediaTypeUploadTo(), validators=[validate_media_file])
    duracao_video = models.PositiveSmallIntegerField(_('Duração do vídeo (em milissegundos):'), null=True, blank=True)
    desc_imagem = models.CharField(_('Descrição da Imagem:'), max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Noticía'
        verbose_name_plural = 'Noticías'

    def __str__(self):
        return self.titulo

    
class Patrocinador(models.Model):

    nome = models.CharField(_('Nome:'), max_length=18, default='')
    logo = models.ImageField(_('Logo:'), upload_to='main/images/patrocinadores')
    link = models.URLField(_('Link:'), max_length=200, default='')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Patrocinador'
        verbose_name_plural = 'Patrocinadores'