from random import randint
import time
from typing import List
import uuid

from utils.interfaces import Observer, Subject
from utils.movement_states import ElevatorState, StoppedState
from utils.weight_sensor import WeightSensor


class Elevator(Subject):
    elevator_id: str
    num_floors: int
    current_floor: int
    previous_state: ElevatorState
    current_state: ElevatorState
    elevator_velocity: float
    weight_sensor: WeightSensor
    requested_floors: List[int]
    observers: List[Observer]

    def __init__(self, num_floors: int, weight_sensor: WeightSensor) -> None:
        self.num_floors = num_floors
        self.current_floor = 0
        self.current_state = StoppedState()
        self.previous_state = None
        self.elevator_id = str(uuid.uuid4())[:8]
        self.weight_sensor = weight_sensor
        self.elevator_velocity = 1
        self.requested_floors = []
        self.observers = []

    def press_floor_number_button(self, floor: int):
        if floor == self.current_floor:
            return
        self.requested_floors.append(floor)
        self.weight_sensor.set_weight(sum(self.weight_dict.values()))

    def press_call_button(self, floor: int):
        if floor == self.current_floor:
            return
        self.requested_floors.append(floor)

    # State methods
    def elevador_step(self):
        self.__set_velocity()
        time.sleep(self.elevator_velocity)
        self.current_state.elevator_step(self)

    def __set_velocity(self):
        weight = self.weight_sensor.get_weight()
        if weight > 30:
            self.elevator_velocity = 1
        elif weight >= 20:
            self.elevator_velocity = 0.3
        else:
            self.elevator_velocity = 0.15

    def emergency_button(self):
        self.current_state.emergency_button(self)

    # Subject methods
    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)
