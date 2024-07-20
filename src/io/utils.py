import os


def load_instance_as_list(file_path: str):
    '''
    returns:
        - nr_of_jobs: str
        - nr_of_machines: str
        - operations: List
            [
            [(machine_id processing_time),(),(),()], <-- job 1
            [(),(),(),()], <-- job 2
            ...
            ]
    '''
    #print(f"Loading: {file_path}...\n")
    with open(file_path) as f:
        lines = f.readlines()

    first_line = lines[0].split()

    # Number of jobs
    nr_of_jobs = int(first_line[0])
    # Number of machines. This is also often referred to as number of operations
    nr_of_machines = int(first_line[1])

    #stripped_list = [] # removed new line chars \n
    job_list = [ [] for _ in range(nr_of_jobs) ] # Create nest list with nr_of_jobs arrays

    job_list_index = 0
    for line in lines[1:]: # do not include the first row (that's meta info)
        stripped_line = line.strip()
        elements = stripped_line.split() # elements = array containing every integer of the given job
        for i in range(0, len(elements), 2):
            machine_id = int(elements[i])
            processing_time = int(elements[i+1])
            job_list[job_list_index].append((machine_id, processing_time))
        job_list_index += 1

    return nr_of_jobs, nr_of_machines, job_list

def get_all_file_paths(data_folder: str, absolute_paths=True):
    '''
    Get all file paths in data_folder. Get absolute path to files
    if absolute_paths=True
    '''
    # Ensure the data_folder is a valid directory
    if not os.path.isdir(data_folder):
        raise ValueError(f"The specified path '{data_folder}' is not a valid directory.")

    # List all files and directories in the specified folder
    filenames = os.listdir(data_folder)
    
    # If you want to include the full path of each file
    if absolute_paths:
        absolute_paths = [os.path.abspath(os.path.join(data_folder, file)) for file in filenames]
        return absolute_paths

    relative_paths = [os.path.join(data_folder, file) for file in filenames]
    return relative_paths