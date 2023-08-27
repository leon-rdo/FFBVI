from django.db import models
from django.utils.translation import gettext_lazy as _

class Saida(models.Model):

    descricao = models.CharField(_("Descrição da saída:"), max_length=255)
    valor = models.DecimalField(_("Valor da saída:"), max_digits=5, decimal_places=2)
    data = models.DateField(_("Data"), auto_now_add=True)
    partida = models.ForeignKey("main.Partida", null=True, blank=True, verbose_name=_("Partida"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Saída")
        verbose_name_plural = _("Saídas")

    def __str__(self):
        return self.descricao