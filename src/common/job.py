from typing import List
from src.common.operation import Operation


class Job:
    def __init__(self, id: int):
        self._id = id
        self._operations: List[Operation] = [] # Implements the precedence constraint (sequence of operations)
        self._current_op_index = 0 # Represents the index of the active operation index

    def add_operation(self, operation: Operation) -> None:
        """Add an operation to the job."""
        self._operations.append(operation)

    @property
    def nr_of_operations(self) -> int:
        """Return the number of operations for that job."""
        return len(self.operations)
    
    @property
    def operations(self) -> List[Operation]:
        """Return a list of all operations for that job."""
        return self._operations
    
    @property
    def id(self) -> int:
        """Return the ID of the job."""
        return self._id
    
    @property
    def current_op_index(self) -> int:
        """Return the index of the current operation."""
        return self._current_op_index
    
    @property
    def scheduled_operations(self) -> List[Operation]:
        """Return a list of operations that were already scheduled."""
        return [operation for operation in self.operations if operation.was_scheduled]

    @property
    def next_earliest_start_time(self) -> int:
        """Returns the end_time of the latest scheduled operation. This is also the earliest start_time of the next operation."""
        #return max([operation.end_time for operation in self.scheduled_operations], default=0) # Iterations me not likey :(
        return self.operations[self.current_op_index - 1].end_time

    def get_operation(self, operation_id: int) -> Operation:
        """Return operation with operation id."""
        for operation in self.operations:
            if operation.id == operation_id:
                return operation

    def get_current_operation(self) -> Operation:
        if self.current_op_index < len(self.operations):
            return self.operations[self.current_op_index]
        return None

    def complete_current_operation(self) -> None:
        self._current_op_index += 1

    def has_more_operations(self) -> bool:
        return self.current_op_index < len(self.operations)

    def reset(self) -> None:
        self._current_op_index = 0 # Reset the index to the first operation
        for operation in self.operations:
            operation.reset()

    def __str__(self):
        operations_str = ', '.join([f'(Machine: {op.machine_id}, Processing Time: {op.processing_time})' for op in self.operations])
        return f"Job {self.id}: {operations_str}\n\n"
    
    def __repr__(self):
        return self.__str__()