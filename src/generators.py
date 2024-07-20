import random
import matplotlib.pyplot as plt

class JobShopGenerator:
    @staticmethod
    def initialize_seed(seed):
        random.seed(seed)

    @staticmethod
    def uniform_random(a, b):
        return random.randint(a, b)

    @staticmethod
    def generate_processing_times_taillard(seed_time, n_jobs, n_machines, min_time=1, max_time=99):
        JobShopGenerator.initialize_seed(seed_time)
        processing_times = [
            [JobShopGenerator.uniform_random(min_time, max_time) for _ in range(n_jobs)]
            for _ in range(n_machines)
        ]
        return processing_times

    @staticmethod
    def generate_processing_times_demirkol(n_jobs, n_machines, min_time=1, max_time=200):
        processing_times = [
            [JobShopGenerator.uniform_random(min_time, max_time) for _ in range(n_machines)]
            for _ in range(n_jobs)
        ]
        return processing_times

    @staticmethod
    def generate_machine_assignments(seed_machine, n_jobs, n_machines):
        machine_assignments = [
            [i for i in range(n_machines)]
            for _ in range(n_jobs)
        ]
        JobShopGenerator.initialize_seed(seed_machine)
        for j in range(n_jobs):
            for i in range(n_machines):
                k = JobShopGenerator.uniform_random(i, n_machines - 1)
                machine_assignments[j][i], machine_assignments[j][k] = (
                    machine_assignments[j][k],
                    machine_assignments[j][i],
                )
        return machine_assignments

    @staticmethod
    def generate_job_routings(n_jobs, n_machines, job_type='classic'):
        job_routings = []
        if job_type == 'classic':
            for job in range(n_jobs):
                job_routings.append(random.sample(range(n_machines), n_machines))
        elif job_type == 'two-set':
            set1_size = n_machines // 2
            set2_size = n_machines - set1_size
            for job in range(n_jobs):
                set1 = random.sample(range(set1_size), set1_size)
                set2 = random.sample(range(set1_size, set1_size + set2_size), set2_size)
                job_routings.append(set1 + set2)
        return job_routings

    @staticmethod
    def format_instance(processing_times, machine_assignments):
        n_machines = len(processing_times)
        n_jobs = len(processing_times[0])
        formatted_instance = []
        for j in range(n_jobs):
            job = []
            for i in range(n_machines):
                machine = machine_assignments[j][i]
                processing_time = processing_times[machine][j]
                job.append((machine, processing_time))
            formatted_instance.append(job)
        return formatted_instance

    @staticmethod
    def format_instance_demirkol(processing_times, job_routings):
        n_jobs = len(processing_times)
        n_machines = len(processing_times[0])
        formatted_instance = []
        for job in range(n_jobs):
            job_operations = []
            for idx, machine in enumerate(job_routings[job]):
                processing_time = processing_times[job][idx]
                job_operations.append((machine, processing_time))
            formatted_instance.append(job_operations)
        return formatted_instance

    @staticmethod
    def store_instance(formatted_instance, filename):
        n_jobs = len(formatted_instance)
        n_machines = len(formatted_instance[0])
        with open(filename, 'w') as file:
            file.write(f"{n_jobs} {n_machines}\n")
            for job in formatted_instance:
                line = " ".join(f"{machine} {time}" for machine, time in job)
                file.write(f"{line}\n")

    @staticmethod
    def generate_taillard(seed_time, seed_machine, n_jobs, n_machines):
        processing_times = JobShopGenerator.generate_processing_times_taillard(seed_time, n_jobs, n_machines)
        machine_assignments = JobShopGenerator.generate_machine_assignments(seed_machine, n_jobs, n_machines)
        formatted_instance = JobShopGenerator.format_instance(processing_times, machine_assignments)
        return formatted_instance

    @staticmethod
    def generate_demirkol(n_jobs, n_machines, min_time=1, max_time=200, job_type='classic'):
        processing_times = JobShopGenerator.generate_processing_times_demirkol(n_jobs, n_machines, min_time, max_time)
        job_routings = JobShopGenerator.generate_job_routings(n_jobs, n_machines, job_type)
        formatted_instance = JobShopGenerator.format_instance_demirkol(processing_times, job_routings)
        return formatted_instance
    
class JobShopScheduler:
    @staticmethod
    def first_in_first_out(jobs):
        return sorted(jobs, key=lambda job: job['arrival'])

    @staticmethod
    def last_in_first_out(jobs):
        return sorted(jobs, key=lambda job: job['arrival'], reverse=True)

    @staticmethod
    def shortest_processing_time(jobs):
        return sorted(jobs, key=lambda job: job['operations'][0]['processing_time'])

    @staticmethod
    def random_order(jobs):
        jobs_copy = jobs[:]
        random.shuffle(jobs_copy)
        return jobs_copy

    @staticmethod
    def most_work_remaining(jobs):
        return sorted(jobs, key=lambda job: sum(op['processing_time'] for op in job['operations']), reverse=True)

    @staticmethod
    def schedule_jobs(jobs, rule):
        if rule == 'fifo':
            return JobShopScheduler.first_in_first_out(jobs)
        elif rule == 'lifo':
            return JobShopScheduler.last_in_first_out(jobs)
        elif rule == 'spt':
            return JobShopScheduler.shortest_processing_time(jobs)
        elif rule == 'random':
            return JobShopScheduler.random_order(jobs)
        elif rule == 'mwr':
            return JobShopScheduler.most_work_remaining(jobs)
        else:
            raise ValueError("Unknown dispatching rule")
        
    @staticmethod
    def create_gantt_chart(jobs, filename="gantt_chart.png"):
        fig, gnt = plt.subplots()

        # Setting labels for x-axis and y-axis
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Machines')

        # Setting ticks on y-axis
        gnt.set_yticks([i for i in range(len(jobs[0]['operations']))])
        gnt.set_yticklabels([f'Machine {i}' for i in range(len(jobs[0]['operations']))])

        # Setting grid
        gnt.grid(True)

        # Creating Gantt chart
        for job in jobs:
            start_time = 0
            for op in job['operations']:
                gnt.broken_barh([(start_time, op['processing_time'])], (op['machine'] - 0.4, 0.8), facecolors=('tab:blue'))
                start_time += op['processing_time']

        plt.savefig(filename)
        plt.show()


if __name__ == '__main__':
    seed_time = 123456
    seed_machine = 654321
    n_jobs = 5
    n_machines = 3

    taillard_instance = JobShopGenerator.generate_taillard(seed_time, seed_machine, n_jobs, n_machines)
    print(f"Generated Taillard instance: {taillard_instance}")
    JobShopGenerator.store_instance(taillard_instance, f"./data/generated/taillard_generated_sample_instance_{n_jobs}x{n_machines}.txt")

    demirkol_instance = JobShopGenerator.generate_demirkol(n_jobs, n_machines, job_type='classic')
    print(f"Generated Demirkol instance: {demirkol_instance}")
    JobShopGenerator.store_instance(demirkol_instance, f"./data/generated/demirkol_generated_sample_instance_{n_jobs}x{n_machines}.txt")


    # Convert formatted_instance to a suitable format for scheduling
    jobs = []
    for job_id, operations in enumerate(taillard_instance):
        job = {
            'job': job_id,
            'arrival': job_id,  # Assuming arrival order is the same as job_id for simplicity
            'operations': [{'machine': op[0], 'processing_time': op[1]} for op in operations]
        }
        jobs.append(job)

    # Applying different dispatching rules and creating Gantt charts
    rules = ['fifo', 'lifo', 'spt', 'random', 'mwr']
    for rule in rules:
        print(f"\n{rule.upper()}:")
        scheduled_jobs = JobShopScheduler.schedule_jobs(jobs, rule)
        for job in scheduled_jobs:
            print(job)
        JobShopScheduler.create_gantt_chart(scheduled_jobs, filename=f"gantt_chart_{rule}.png")