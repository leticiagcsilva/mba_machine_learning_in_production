import time
from utils.interfaces import Observer
from utils.interfaces import Subject


class ButtonCallElevator(Subject):
    def __init__(self, floor):
        self.floor = floor
        self.is_pressed = False
        self.__list_of_observers = []

    def attach(self, observer):
        self.__list_of_observers.append(observer)

    def detach(self, observer):
        self.__list_of_observers.remove(observer)

    def notify(self):
        for observer in self.__list_of_observers:
            observer.update(self)

    def press_button(self):
        self.is_pressed = True
        self.notify()


class DoorElevator(Observer):
    def __init__(self, floor, button):
        self.floor = floor
        self.is_open = False

    def __open_door(self):
        print(f'PORTA {self.floor} -> ABRINDO...')
        time.sleep(0.5)
        print(f'PORTA {self.floor} == ABERTA!')
        self.is_open = True

    def __close_door(self):
        print(f'PORTA {self.floor} -> FECHANDO...')
        self.is_open = False
        time.sleep(0.5)
        print(f'PORTA {self.floor} == FECHADA!')

    def get_is_open(self):
        return self.is_open

    def update(self, subject):
        actual_state_stopped = isinstance(subject.current_state, StoppedState)
        right_floor = subject.current_floor == self.floor
        reach_a_target_floor = len(
            subject.requested_floors) < self.__previous_len_requests

        if right_floor and actual_state_stopped and len(subject.requested_floors) == 0:
            self.__open_door()
            time.sleep(3)
            return

        if right_floor and actual_state_stopped and len(subject.requested_floors) > 0 and self.is_open:
            self.__close_door()
            time.sleep(3)
            return

        if right_floor and actual_state_stopped and reach_a_target_floor:
            self.__open_door()
            time.sleep(3)
            self.__close_door()
            return

        if right_floor and actual_state_stopped and subject.previous_state is None:
            self.__close_door()
            return

        self.__previous_len_requests = len(subject.requested_floors)
