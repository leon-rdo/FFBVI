from main.models import Patrocinador

def patrocinadores(request):
    patrocinadores = Patrocinador.objects.all()
    return {'patrocinadores': patrocinadores}