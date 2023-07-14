from datetime import date
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

class Patrocinador(models.Model):

    nome = models.CharField(max_length=50, default='')
    logo = models.ImageField(upload_to='main/images/patrocinadores')
    link = models.URLField(max_length=200, default='')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Patrocinador'
        verbose_name_plural = 'Patrocinadores'

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
    nome_jogador = models.CharField(default='', max_length=50, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    tipo = models.CharField(default='federado', max_length=50, choices=TIPO)
    # Informações de Contato
    email = models.EmailField(max_length=254, null=True, blank=True)
    telefone = models.CharField(max_length=20, validators=[telefone_validator], null=True, blank=True)
    # Informações Físicas
    foto_principal = models.ImageField(upload_to='main/foto_jogador', null=True, blank=True)
    foto_secundaria = models.ImageField(upload_to='main/foto_jogador', null=True, blank=True)
    altura = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    # Informações de Nascimento
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    uf_nascimento = models.CharField(max_length=20, choices=UF_CHOICES, null=True, blank=True)
    cidade_nascimento = models.CharField(max_length=50, null=True, blank=True)
    # Informações de Futebol
    posicao = models.CharField(max_length=50, choices=POSICOES)
    time_coracao = models.CharField(max_length=50, choices=TIMES, null=True, blank=True)
    gols_marcados = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    pontos = models.SmallIntegerField(default=0, null=True, blank=True)

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
    data = models.DateField(auto_now=False, auto_now_add=False, null=True)
    hora = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    relacionados = models.ManyToManyField(User, related_name='relacionados', blank=True)
    time_verde = models.ManyToManyField(User, related_name='partidas_timeA', blank=True)
    time_vermelho = models.ManyToManyField(User, related_name='partidas_timeB', blank=True)
    time_azul = models.ManyToManyField(User, related_name='partidas_timeC', blank=True)
    sorteada = models.BooleanField(default=False)

    slug = models.SlugField(max_length=50, unique=True, editable=False, default='')

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
        
class Pagamento(models.Model):

    comprovante = models.ImageField(upload_to='main/images/pagamentos', blank=True, null=True)
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    em_dinheiro = models.BooleanField(default=False)

    def __str__(self):
        return self.jogador.nome_jogador

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
    
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

    telefone_diretor = models.CharField(max_length=100)
    email_diretor = models.EmailField()
    qr_code_pagamento = models.ImageField(upload_to='main/images/')
    regras_federacao = models.TextField()
    alerta_mensagem = models.CharField(max_length=100, blank=True, null=True)
    alerta_link = models.URLField(max_length=200, blank=True, null=True)
    alerta_texto_link = models.CharField(max_length=50, blank=True, null=True)
    alerta_cor = models.CharField(default='warning', max_length=50, choices=ALERTA_CORES, blank=True, null=True)
    alerta_icon = models.CharField(default=None, max_length=50, choices=ALERTA_ICONES, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Configurações'

    def save(self, *args, **kwargs):
        if not self.pk and Configuracao.objects.exists():
            return Configuracao.objects.first()
        return super().save(*args, **kwargs)