from typing import List
from utils.elevator import Elevator
from utils.communication_system import CommunicationSytem
from utils.multimidia_system import MultimidiaSystem
from utils.elevator_door import ButtonCallElevator, DoorElevator
from utils.weight_sensor import WeightSensor


class GenericElevadorSystem:
    def run(self, requested_floor: List[int]) -> str:
        raise NotImplementedError()

    def call(self, requested_floor: int, target_floor: int) -> str:
        raise NotImplementedError()


class GenericElevadorSystemFactory:
    def factory_method(self) -> GenericElevadorSystem:
        raise NotImplementedError()


class ElevadorSystemFactory(GenericElevadorSystemFactory):
    def factory_method(self, num_floors) -> GenericElevadorSystem:
        return ElevatorSystem(num_floors)


class ElevatorSystem(GenericElevadorSystem):
    def __init__(self, floors_num: int):
        self.floor_doors = []
        weight_sensor = WeightSensor()
        self.elevator = Elevator(floors_num, weight_sensor)
        self.communication_system = CommunicationSytem()
        self.multimidia_system = MultimidiaSystem()
        for i in range(floors_num + 1):
            button_door_floor = ButtonCallElevator(i)
            button_door_floor.attach(self.elevator)
            self.floor_doors.append(DoorElevator(i, button_door_floor))
        self.configure_elevator()

    def configure_elevator(self):
        self.elevator.attach(self.communication_system)
        self.elevator.attach(self.multimidia_system)
        for door in self.floor_doors:
            self.elevator.attach(door)

    def press_floor_button(self, floor):
        self.floor_doors[floor].button.press_button()

    def run(self, requested_floor: List[int]) -> str:
        print()
        print("#" * 50)
        print(
            f"\tANDARES SOLICITADOS: {', '.join(str(f) for f in requested_floor)}")
        print("#" * 50, "\n")
        _ = [self.elevator.press_floor_number_button(
            floor) for floor in requested_floor]

        cond_1, cond_2 = True, True
        while cond_1 and cond_2:
            current_state = isinstance(
                self.elevator.current_state, StoppedState)
            previous_state = isinstance(
                self.elevator.previous_state, StoppedState)
            cond_1 = not (current_state and previous_state)
            cond_2 = len(self.elevator.requested_floors) > 0
            self.elevator.elevador_step()

    def call(self, requested_floor: int, target_floor: int) -> str:
        print()
        print("#"*20)
        print(f'\tANDAR CHAMADO: {requested_floor}')
        print("#"*20, "\n")
        self.elevator.press_call_button(requested_floor)
        cond_1, cond_2 = True, True
        while cond_1 and cond_2:
            current_state = self.elevator.current_state.__class__.__name__ == "StoppedState"
            previous_state = self.elevator.previous_state.__class__.__name__ == "StoppedState"
            cond_1 = not (current_state and previous_state)
            cond_2 = len(self.elevator.requested_floors) > 0
            self.elevator.elevador_step()
            
        self.run([target_floor])
        return f"O elevador chegou ao andar {target_floor}"
