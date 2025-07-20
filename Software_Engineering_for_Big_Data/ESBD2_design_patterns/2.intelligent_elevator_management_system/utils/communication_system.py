from utils.interfaces import Observer


class CommunicationSystem(Observer):
    def __init__(self):
        self.is_emergency: bool = False
        self.is_maintenance: bool = False

    def update(self, subject) -> None:
        if subject.is_emergency:
            print('Central de Inteligencia: Elevador em emergencia')
            self.send_emergency_call()
        elif subject.is_maintenance:
            print('Central de Inteligencia: Elevador em manutenção')
            print('Acionar sistema de portas para fechar')

    def send_emergency_call(self) -> None:
        print("Enviando chamado de emergencia para equipe de manutenção")
