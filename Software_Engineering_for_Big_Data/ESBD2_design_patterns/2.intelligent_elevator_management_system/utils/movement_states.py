from abc import ABC, abstractmethod
import time


class Singleton:

    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class ElevatorState(ABC, Singleton):

    @abstractmethod
    def elevator_step(self, elevator):
        raise NotImplementedError


    def emergency_button(self, elevator):
        print("Elevador em emergência")
        elevator.current_state = StoppedState()
        elevator.requested_floors = []
        elevator.is_emergency = True
        elevator.notify()


    def maintenance_button(self, elevator):
        print("Elevador em manutenção")
        elevator.current_state = StoppedState()
        elevator.requested_floors = []
        elevator.is_maintenance = True
        elevator.notify()

class MovingUpState(ElevatorState):
    def elevator_step(self, elevator):
        required_floors = elevator.requested_floors
        target = min([i for i in required_floors if i >= elevator.current_floor])
        elevator.current_floor += 1
        elevator.weight_sensor.set_weight(sum(elevator.weight_dict.values()))
        print(f"{elevator.current_floor - 1} -> {elevator.current_floor}. Peso: {elevator.weight_sensor.get_weight()} Kg")
        if elevator.current_floor == target:
            elevator.requested_floors.remove(target)
            elevator.previous_state, elevator.current_state = self, StoppedState()
        else:
            elevator.current_state = MovingUpState()


class MovingDownState(ElevatorState):
    def elevator_step(self, elevator):
        if len(elevator.requested_floors) == 0:
            elevator.previous_state, elevator.current_state = self, StoppedState()
            return
        target = max(
            [i for i in elevator.requested_floors if i < elevator.current_floor])
        elevator.current_floor -= 1
        elevator.weight_dict[elevator.current_floor] = 0
        elevator.weight_sensor.set_weight(sum(elevator.weight_dict.values()))
        print(f"{elevator.current_floor + 1} -> {elevator.current_floor}. Peso: {elevator.weight_sensor.get_weight()} Kg")

        if elevator.current_floor == target:
            elevator.requested_floors.remove(target)
            elevator.previous_state, elevator.current_state = self, StoppedState()
        else:
            elevator.previous_state, elevator.current_state = self, MovingDownState()


class StoppedState(ElevatorState):
    def elevator_step(self, elevator):
        required_floors = elevator.requested_floors
        actual_floor = elevator.current_floor

        elevator.notify()

        if len(elevator.requested_floors) == 0:
            return

        max_greater_than = max(required_floors) > actual_floor
        min_greater_than = min(required_floors) > actual_floor
        max_less_than = max(required_floors) < actual_floor
        min_less_than = min(required_floors) < actual_floor

        elevator.weight_dict[actual_floor] = 0

        if max_greater_than and min_greater_than:
            elevator.previous_state, elevator.current_state = self, MovingUpState()
        elif max_less_than and min_less_than:
            elevator.previous_state, elevator.current_state = self, MovingDownState()
        elif elevator.previous_state == MovingDownState() and max_greater_than:
            elevator.previous_state, elevator.current_state = self, MovingDownState()
        elif elevator.previous_state == MovingUpState() and max_less_than:
            elevator.previous_state, elevator.current_state = self, MovingUpState()
        else:
            elevator.previous_state, elevator.current_state = self, MovingUpState()
            return
