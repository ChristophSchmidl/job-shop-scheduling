from __future__ import unicode_literals
import argparse
import json
import os
import csv
from collections import deque
import numpy as np
from src.io.utils import load_instance_as_list
from src.common.job_shop import JobShop
from src.common.dispatcher import Dispatcher


def createParser():
    parser = argparse.ArgumentParser(description='Job-Shop-Scheduling')
    parser.add_argument('--input', '-i',
                        type=str,
                        action='store',
                        default="ta01",
                        help='Input File')
    parser.add_argument('--output', '-o',
                        type=str,
                        action='store',
                        default='./output/results.csv',
                        required=False,
                        help='csv Schedule File')
    parser.add_argument('--algorithm', '-a',
                        type=str,
                        action='store',
                        default='fifo',
                        required=False,
                        help='algorithm choice from [fifo, lifo, mwkr, lwkr, random]')
    parser.add_argument('--show_plots', '-sp',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Show Gantt chart plots after each dispatching rule. Default is False and only saves plots.')
    parser.add_argument('--show_instances', '-si',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Show all available instances from instances.json')
    parser.add_argument('--verify_instances', '-vi',
                        action='store_true',
                        default=False,
                        required=False,
                        help='Verify all instances present in instances.json')
    return parser

def get_nested(data, keys):
    """
    Retrieve value from nested dictionary.
    
    Parameters:
    - data: The dictionary to search.
    - keys: A list of keys representing the path in the nested dictionary.
    
    Returns:
    - The value at the specified path or None if any key in the path does not exist.
    """
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            return None
    return data

def get_all_instances():
    instance_file = open(os.path.join(os.path.dirname( __file__ ), './instances.json'),"r")
    json_data = json.load( instance_file )

    json_instances = [ inst for inst in json_data ]
    return json_instances

def get_all_instances_as_dict():
     json_instances = get_all_instances()
     # Preprocess data into a dictionary for efficient lookup
     benchmark_dict = {entry['name']: entry for entry in json_instances}
     return benchmark_dict

def get_jobshop_instance(instance_name: str) -> JobShop:
    benchmark_dict = get_all_instances_as_dict()

    if instance_name not in benchmark_dict:
        raise KeyError(f"Instance '{instance_name}' not found in benchmark data.")
    
    benchmark_instance = benchmark_dict.get(instance_name)
    job_shop = JobShop(file_path=benchmark_instance.get("path", None),
                            name=benchmark_instance.get("name", None),
                            optimum=benchmark_instance.get("optimum", None),
                            info=benchmark_instance.get("info", None),
                            author=benchmark_instance.get("author", None),
                            upper_bound=get_nested(benchmark_dict, "upper"),
                            lower_bound=get_nested(benchmark_dict, "lower"))
    return job_shop

def write_to_csv(output_file, results):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Algorithm', 'Instance', 'Makespan'])
        for result in results:
            writer.writerow(result)

def main():
    # parse args
    parser = createParser()
    args = parser.parse_args()

    if args.verify_instances:
        """
        Verify that the file exists and the number of jobs
        and machines match.
        """
        json_instances = get_all_instances()

        for instance in json_instances:
            instance_path = instance['path']
            instance_name = instance["name"]
            instance_jobs = instance["jobs"]
            instance_machines = instance["machines"]

            if os.path.isfile(instance_path):
                nr_of_jobs, nr_of_machines, job_list = load_instance_as_list(instance_path)
                if nr_of_jobs != instance_jobs or nr_of_machines != instance_machines:
                    print(f"Verify: {instance_name}, {instance_path}\t \u274C")
                    break
            else:
                raise FileNotFoundError(f"File not found: {instance_path}.")
            
            print(f"Verify: {instance_name}, {instance_path}\t \u2705")
        print(f"Verified {len(json_instances)} instances in total.")
        exit()

    if args.show_instances:
        json_instances = get_all_instances()

        current_author = ""
        for instance in json_instances:
            if current_author != instance["author"]:
                current_author = instance["author"]
                print(f"\n\t*** Benchmark instances by {current_author} ***\n")

            print(
                f"Name: {instance['name']}, "
                f"Jobs: {instance['jobs']}, "
                f"Machines: {instance['machines']}, "
                f"Path: {instance['path']}"
            )
        print(f"{len(json_instances)} instances in total.")
        exit()

    if args.input:
        jobshop_instance = get_jobshop_instance(args.input.lower())

    results = []

    if args.algorithm:
        dispatcher = Dispatcher(jobshop_instance)
        algorithms = ["fifo", "lifo", "mwkr", "lwkr", "random"] if args.algorithm.lower() == "all" else [args.algorithm.lower()]

        for algo in algorithms: # match = Python 3.10 feature
            jobshop_instance.reset()
            match algo:
                case "fifo":
                    print("Dispatching rule: FIFO")
                    makespan = dispatcher.fifo()
                case "lifo":
                    print("Dispatching rule: LIFO")
                    makespan = dispatcher.lifo()
                case "mwkr":
                    print("Dispatching rule: MWKR")
                    makespan = dispatcher.mwkr()
                case "lwkr":
                    print("Dispatching rule: LWKR")
                    makespan = dispatcher.lwkr()
                case "random":
                    print("Dispatching rule: Random")
                    makespan = dispatcher.random()
                case _:
                    print(f"Unknown algorithm: {algo}")
                    continue

            print(f"Makespan for instance {jobshop_instance.file_path} using {algo.upper()}: {makespan}")
            print(f"Verification of {algo.upper()} schedule: {jobshop_instance.verify_schedule()}")
            dispatcher.plot_gantt_chart()
            results.append([algo, jobshop_instance.name, makespan])

        if args.output:
            write_to_csv(args.output, results)
                

if __name__ == "__main__":
    main()