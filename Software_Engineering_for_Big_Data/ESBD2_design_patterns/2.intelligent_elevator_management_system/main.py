import random
from utils.elevator_system import GenericElevadorSystem, GenericElevadorSystemFactory, ElevadorSystemFactory

if __name__ == "__main__":
    num_floors = 20

    elevator_system_factory = ElevadorSystemFactory()
    elevator_system_1 = elevator_system_factory.factory_method(num_floors)

    requested_floors = random.sample(range(num_floors), random.randint(1, 3))

    #elevator_system_1.run(requested_floors)
    elevator_system_1.elevator.emergency_button()