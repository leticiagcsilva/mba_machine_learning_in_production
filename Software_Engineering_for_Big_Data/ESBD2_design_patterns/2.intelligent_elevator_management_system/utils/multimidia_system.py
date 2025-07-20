import os
from utils.interfaces import Observer


class MultimidiaSystem(Observer):

    def _play_music(self):
        print('Música de espera.')
        musica = "musica.mp3"
        os.system(musica)

    def _play_voice(self):
        print('Aviso aos passageiros')

    def update(self, subject):
        if subject.is_emergency:
            print('Emergência')
            self._play_voice()
            self._play_music()
