from django.views.generic import TemplateView
from main.models import Pagamento, Partida

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagamentos"] = Pagamento.objects.all()
        context["partidas"] = Partida.objects.all()
        return context
    