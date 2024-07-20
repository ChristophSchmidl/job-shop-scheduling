from typing import List
from src.common.operation import Operation


class Machine:
    def __init__(self, machine_id):
        self._id = machine_id
        self._schedule = [] # A list of operations

    @property
    def id(self) -> int:
        """Return the ID of the machine."""
        return self._id
    
    @property
    def schedule(self) -> List[Operation]:
        """Return a list of all operations already scheduled for the machine."""
        return self._schedule

    def is_available(self, start_time: int) -> bool:
        """This method is not really needed right now but nice to have :)"""
        if not self.schedule:
            return True
        last_operation = self.schedule[-1]
        can_schedule = last_operation.end_time <= start_time
        return can_schedule
    
    @property
    def next_earliest_start_time(self) -> int:
        """
        Returns the end_time of the latest scheduled operation on that machine. 
        This is also the earliest start_time of the next operation.
        """
        if not self.schedule:
            return 0
        return self.schedule[-1].end_time

    def schedule_operation(self, operation: Operation, start_time: int) -> Operation:
        operation.schedule(start_time) # set start_time, end_time, was_scheduled
        self.schedule.append(operation) # Put operation at the end of the machine schedule
        
        return operation
    
    def reset(self) -> None:
        self._schedule = []

    def __str__(self):
        operations_str = ', '.join([f'{op}' for op in self.schedule])
        return f"Machine with ID {self.machine_id} and schedule: {operations_str}"