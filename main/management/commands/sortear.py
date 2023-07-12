from django.core.management.base import BaseCommand
from main.models import Partida
from random import choice, shuffle
import datetime

class Command(BaseCommand):
    help = 'Sorteia jogadores da partida da semana nos três times.'

    def handle(self, *args, **options):
        today = datetime.date.today()
        partida = Partida.objects.filter(data=today, sorteada=False).first()

        if partida:
            # Crie uma lista com os usuários relacionados
            relacionados = list(partida.relacionados.all())

            # Separe os jogadores de posição "goleiro" dos jogadores restantes
            goleiros = []
            jogadores = []
            for relacionado in relacionados:
                if relacionado.posicao == 'goleiro':
                    goleiros.append(relacionado)
                else:
                    jogadores.append(relacionado)

            # Embaralhe as duas listas separadamente
            shuffle(goleiros)
            shuffle(jogadores)

            # Verifique se há 3 goleiros na lista
            if len(goleiros) == 3:
                # Redistribua os goleiros nos três times
                times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                shuffle(times)
                times[0].set([goleiros[0]])
                times[1].set([goleiros[1]])
                times[2].set([goleiros[2]])
                self.stdout.write(self.style.WARNING('Há três goleiros.'))
                
            # Verifique se há 2 goleiros para sortear
            elif len(goleiros) == 2:
                # Atribua os goleiros aleatoriamente a dois dos times
                times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                shuffle(times)
                times_escolhidos = [times[0], times[1]]
                times_escolhidos[0].set([goleiros[0]])
                times_escolhidos[1].set([goleiros[1]])
                self.stdout.write(self.style.WARNING('Há dois goleiros.'))

            # Verifique se há 1 goleiros para sortear
            elif len(goleiros) == 1:
                # Atribua o único goleiro aleatoriamente a um dos times
                times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                time_escolhido = choice(times)
                time_escolhido.set([goleiros[0]])
                self.stdout.write(self.style.WARNING('Há um goleiro.'))
                
            # Verifique se há mais de 3 goleiros para sortear
            elif len(goleiros) > 3:
                # Redistribua os goleiros nos três primeiros times
                times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                shuffle(times)
                times[0].set([goleiros[0]])
                times[1].set([goleiros[1]])
                times[2].set([goleiros[2]])

                # Distribua os goleiros restantes aleatoriamente nos times
                for goleiro in goleiros[3:]:
                    time_escolhido = choice(times)
                    time_escolhido.add(goleiro)
                    
                self.stdout.write(self.style.WARNING('Há mais de três goleiros.'))

            # Divida a lista em três partes iguais
            terco = len(jogadores) // 3
            partida.time_verde.add(*jogadores[:terco])
            partida.time_vermelho.add(*jogadores[terco:2 * terco])
            partida.time_azul.add(*jogadores[2 * terco:])

            # Marque a partida como sorteada
            partida.sorteada = True
            partida.save()
            self.stdout.write(self.style.SUCCESS('Os relacionados foram distribuídos entre os times!'))
        else:
            self.stdout.write(self.style.ERROR('Não há partida agendada para hoje ou ela já foi sorteada.'))
