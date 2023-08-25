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

            # Verifica a quantidade de goleiros e os distribui entre os times
            match len(goleiros):
                case 3:
                    # Caso haja três, coloca um em cada time
                    times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                    shuffle(times)
                    times[0].set([goleiros[0]])
                    times[1].set([goleiros[1]])
                    times[2].set([goleiros[2]])
                    self.stdout.write(self.style.WARNING(f'Há {len(relacionados)} relacionados, três são goleiros.'))

                case 2:
                    # Caso haja dois, os coloca em dois times randomicamente
                    times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                    shuffle(times)
                    times[0].set([goleiros[0]])
                    times[1].set([goleiros[1]])
                    self.stdout.write(self.style.WARNING(f'Há {len(relacionados)} relacionados, dois são goleiros.'))

                case 1:
                    # Caso haja apenas um, o coloca em um time aleatório
                    times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                    time_escolhido = choice(times)
                    time_escolhido.set([goleiros[0]])
                    self.stdout.write(self.style.WARNING(f'Há {len(relacionados)} relacionados, apenas um goleiro.'))

                case n if n > 3:
                    # Caso haja mais de três, coloca os três primeiros, um em cada time e o resto aleatoriamente
                    times = [partida.time_verde, partida.time_vermelho, partida.time_azul]
                    shuffle(times)
                    times[0].set([goleiros[0]])
                    times[1].set([goleiros[1]])
                    times[2].set([goleiros[2]])

                    for goleiro in goleiros[3:]:
                        time_escolhido = choice(times)
                        time_escolhido.add(goleiro)
                    
                    self.stdout.write(self.style.WARNING(f'Há {len(relacionados)} relacionados, e mais de quatro goleiros.'))

            # Atribua os jogadores restantes aos times, de acordo com a lotação
            for jogador in jogadores:
                if partida.time_verde.count() < 6:
                    partida.time_verde.add(jogador)
                elif partida.time_vermelho.count() < 6:
                    partida.time_vermelho.add(jogador)
                else:
                    partida.time_azul.add(jogador)

            # Marca a partida como sorteada
            partida.sorteada = True
            partida.save()
            self.stdout.write(self.style.SUCCESS('Os relacionados foram distribuídos entre os times!'))
        else:
            self.stdout.write(self.style.ERROR('Não há partida agendada para hoje ou ela já foi sorteada.'))
