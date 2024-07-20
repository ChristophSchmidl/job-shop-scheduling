import random
from typing import Union
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.common.job import Job
from src.common.job_shop import JobShop


class Dispatcher:
    def __init__(self, job_shop: JobShop):
        self.job_shop = job_shop
        self.max_time_jobs = max(sum(op.processing_time for op in job.operations) for job in self.job_shop.jobs)
        self.job_shop.current_time = {job.id: 0 for job in self.job_shop.jobs}  # Initialize current time for each job
        self.used_algo = None
        self.makespan = None

    def dispatch(self, sort_key=None, reverse=False, random_selection=False) -> int:
        job_queue = [job for job in self.job_shop.jobs]
        makespan = 0

        while job_queue:
            feasible_jobs = []

            for job in job_queue:
                operation = job.get_current_operation()
                if operation and self.job_shop.can_schedule_operation(job, operation):
                    feasible_jobs.append(job)

            if not feasible_jobs:
                print(f"No feasible jobs found!")
                break

            if random_selection:
                job = random.choice(feasible_jobs)
            else:
                feasible_jobs.sort(key=sort_key, reverse=reverse)
                job = feasible_jobs.pop(0)

            operation = job.get_current_operation()
            end_time = self.job_shop.schedule_operation(job, operation)
            makespan = max(makespan, end_time)

            if not job.has_more_operations():
                job_queue.remove(job)
        self.makespan = makespan
        return self.makespan

    def fifo(self) -> int:
        self.used_algo = "FIFO"
        return self.dispatch(sort_key=lambda job: self.job_shop.current_time[job.id])
        
    def lifo(self) -> int:
        self.used_algo = "LIFO"
        return self.dispatch(sort_key=lambda job: self.job_shop.current_time[job.id], reverse=True)

    def mwkr(self) -> int:
        self.used_algo = "MWKR"
        return self.dispatch(sort_key=lambda job: self.normalized_remaining_processing_time(job), reverse=True)

    def lwkr(self) -> int:
        self.used_algo = "LWKR"
        return self.dispatch(sort_key=lambda job: self.normalized_remaining_processing_time(job))

    def random(self) -> int:
        self.used_algo = "RANDOM"
        return self.dispatch(random_selection=True)

    def remaining_processing_time(self, job: Job) -> Union[int, float]:
        """ Calculate the total remaining processing time for a job """
        return sum(op.processing_time for op in job.operations[job.current_op_index:])

    def normalized_remaining_processing_time(self, job: Job) -> Union[int, float]:
        """ Calculate the normalized remaining processing time for a job """
        total_processing_time = sum(op.processing_time for op in job.operations)
        remaining_processing_time = self.remaining_processing_time(job)
        return remaining_processing_time / total_processing_time if total_processing_time > 0 else 0

    def scaled_remaining_processing_time(self, job: Job) -> Union[int, float]:
        """ Calculate the scaled remaining processing time for a job """
        total_processing_time = sum(op.processing_time for op in job.operations)

        if total_processing_time == 0:
            return 0

        remaining_percentage = self.normalized_remaining_processing_time(job)
        scaled_remaining_processing_time = (remaining_percentage * self.max_time_jobs) / total_processing_time
        return scaled_remaining_processing_time
    
    def plot_gantt_chart(self, save_plot_only=True) -> None:
        fig, gnt = plt.subplots(figsize=(12, 6))
        nr_of_machines = self.job_shop.nr_of_jobs

        # Setting the labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Machines')

        # Setting the y-ticks to the number of machines
        gnt.set_yticks([i + 1 for i in range(nr_of_machines)])
        gnt.set_yticklabels([f'Machine {i}' for i in range(nr_of_machines)])
        gnt.set_ylim(0, nr_of_machines + 1)

        # Plotting the tasks
        for job in self.job_shop.jobs:
            for operation in job.operations:
                if operation.start_time is not None and operation.end_time is not None:
                    gnt.broken_barh([(operation.start_time, operation.end_time - operation.start_time)], (operation.machine_id + 0.5, 1),
                                    facecolors=(f'C{job.id % 10}'), edgecolor='black')
                    gnt.text(operation.start_time + (operation.end_time - operation.start_time) / 2, operation.machine_id + 1, 
                             f"{job.id}", ha='center', va='center', color='white', fontweight='bold')

        # Adding legend
        handles = [mpatches.Patch(color=f'C{i % 10}', label=f'Job {i}') for i in range(len(self.job_shop.jobs))]
        plt.legend(handles=handles, bbox_to_anchor=(1.01, 1.015), loc='upper left')
        plt.title(f"{self.used_algo} applied to instance {self.job_shop.name} with makespan {self.makespan}")
        plt.grid(True)
        plt.tight_layout(rect=[0, 0, 0.99, 1])  # Adjust layout to make room for the legend

        if save_plot_only:
            plt.savefig(f"./plots/{self.used_algo}_applied_to_{self.job_shop.name}.png", dpi=300)
        else:
            plt.show()