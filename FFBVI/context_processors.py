from main.models import User, Patrocinador

def federados(request):
    federados = User.objects.all()
    return {'users': federados}

def patrocinadores(request):
    patrocinadores = Patrocinador.objects.all()
    return {'patrocinadores': patrocinadores}