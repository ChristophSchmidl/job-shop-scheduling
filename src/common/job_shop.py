from typing import Dict, List
import copy
import random
from src.common.operation import Operation
from src.common.job import Job
from src.common.machine import Machine


class JobShop:
    def __init__(self, file_path, name, optimum, info, author, upper_bound, lower_bound):
        self.file_path = file_path
        self.name = name
        self.jobs = []
        self.machines = {}
        self.nr_of_jobs = 0
        self.nr_of_machines = 0
        self.optimum = optimum
        self.info = info
        self.author = author
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.current_time = {} # dict containing the end_time of last scheduled operation for each job
        self.original_jobs = []
        self.original_machines = {}

        self.load_instance(file_path)

    def load_instance(self, file_path: str) -> None:
        with open(file_path) as f:
            lines = f.readlines()

        first_line = lines[0].split()
        self.nr_of_jobs = int(first_line[0])
        self.nr_of_machines = int(first_line[1])

        self.jobs = []
        self.machines = {}
        op_id = 0
        for job_id in range(self.nr_of_jobs):
            job = Job(job_id)
            elements = lines[job_id + 1].strip().split()
            for i in range(0, len(elements), 2):
                machine_id = int(elements[i])
                processing_time = int(elements[i + 1])
                operation = Operation(op_id, job_id, machine_id, processing_time)
                op_id += 1
                job.add_operation(operation)
                if machine_id not in self.machines:
                    self.machines[machine_id] = Machine(machine_id)
            self.jobs.append(job)
        self.current_time = {job.id: 0 for job in self.jobs}
        self.original_jobs = copy.deepcopy(self.jobs)
        self.original_machines = copy.deepcopy(self.machines)

    def can_schedule_operation(self, job: Job, operation: Operation) -> bool:
        machine = self.machines[operation.machine_id]
        
        # Check if the machine is available
        potential_start_time = machine.next_earliest_start_time
        machine_available = machine.is_available(potential_start_time) # redundant
        
        # Check job precedence using was_scheduled property
        if job.current_op_index > 0:
            prev_operation = job.operations[job.current_op_index - 1]
            prev_operation_finished = prev_operation.was_scheduled
        else:
            prev_operation_finished = True

        return machine_available and prev_operation_finished

    def schedule_operation(self, job: Job, operation: Operation) -> int:
        machine = self.machines[operation.machine_id]
        earliest_start_time = max(self.current_time[job.id], machine.next_earliest_start_time)
        scheduled_operation = machine.schedule_operation(operation, earliest_start_time)
        
        self.current_time[job.id] = scheduled_operation.end_time  # Update the current time for the job
        job.complete_current_operation() # Increase operation pointer by 1

        return scheduled_operation.end_time

    def verify_schedule(self) -> bool:
        # Check for overlapping processing times on the same machine
        for machine in self.machines.values():
            operations = sorted(machine.schedule, key=lambda op: op.start_time)
            for i in range(1, len(operations)):
                prev_op = operations[i - 1]
                curr_op = operations[i]
                if curr_op.start_time < prev_op.end_time:
                    print(f"Overlap detected on machine {machine.machine_id} between operation {prev_op} and {curr_op}")
                    return False

        # Check for order of operations for each job
        for job in self.jobs:
            operations = job.operations
            for i in range(1, len(operations)):
                prev_op = operations[i - 1]
                curr_op = operations[i]
                if prev_op.end_time is not None and curr_op.start_time is not None:
                    if curr_op.start_time < prev_op.end_time:
                        print(f"Order violation detected for job {job.job_id} between operation {prev_op} and {curr_op}")
                        return False
        return True

    def reset(self) -> None:
        self.jobs = copy.deepcopy(self.original_jobs)
        self.machines = copy.deepcopy(self.original_machines)
        self.current_time = {job.id: 0 for job in self.jobs}