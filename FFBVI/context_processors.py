from main.models import Configuracao, Patrocinador

def configuracoes(request):
    configuracoes = Configuracao.objects.first()
    return {'configuracoes': configuracoes}

def patrocinadores(request):
    patrocinadores = Patrocinador.objects.all()
    return {'patrocinadores': patrocinadores}