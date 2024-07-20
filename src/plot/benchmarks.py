from collections import defaultdict
import matplotlib.pyplot as plt
from src.io.utils import get_all_file_paths


def plot_nr_of_jobs(data_folder: str):
    '''
    Example folder: data/demirkol, data/taillard, data/extra
    4. Create dict/set whatever to count overall number of jobs and their occurences
    5. Plot
    '''
    pass

def plot_nr_of_machines(data_folder: str):
    pass

def plot_nr_of_jobs_and_machines(data_folder: str):
    pass



def get_nr_of_jobs(file_paths):
    counts = defaultdict(int)
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                first_integer = int(first_line.split()[0])
                counts[first_integer] += 1
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
    return counts

def get_nr_of_machines(file_paths):
    counts = defaultdict(int)
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                second_integer = int(first_line.split()[1])
                counts[second_integer] += 1
        except Exception as e:
            print(f"Error reading from {file_path}: {e}")
    return counts

def plot_counts(counts, x_label="Job Count", 
                title="Number of jobs and their occurences.", 
                legend_title='Taillard'):
    # Create a larger figure to make the barchart bigger
    plt.figure(figsize=(10, 6))  # Width and height in inches

    # Plot the bar chart
    keys = list(counts.keys())
    values = [counts[key] for key in keys]
    bars = plt.bar(keys, values, tick_label=keys, label=legend_title)

    # Customize plot
    plt.xlabel(x_label)
    plt.ylabel('Occurrences')
    plt.title(title)
    
    # Add labels on top of each bar for clarity
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # Add a legend with the specified title
    plt.legend(title="Benchmarks")

    plt.show()

def plot_side_by_side_counts(counts1, 
                             counts2, 
                             legend_titles=['Data 1', 'Data 2'], 
                             title='Taillard vs Demirkol: Nr of Jobs'):
    # Ensure a consistent set of keys across both dictionaries
    all_keys = sorted(set(counts1.keys()).union(set(counts2.keys())))
    values1 = [counts1.get(key, 0) for key in all_keys]
    values2 = [counts2.get(key, 0) for key in all_keys]

    # X-axis positions for the bars
    x_positions = range(len(all_keys))
    width = 0.35  # Width of the bars

    # Create a larger figure to make the barchart bigger
    plt.figure(figsize=(12, 6))

    # Plot the bars for each dataset
    bars1 = plt.bar(x_positions, values1, width, label=legend_titles[0])
    bars2 = plt.bar([p + width for p in x_positions], values2, width, label=legend_titles[1])

    # Add labels and title
    plt.xlabel('Number of jobs')
    plt.ylabel('Occurrences')
    plt.title(title)
    plt.xticks([p + width / 2 for p in x_positions], all_keys)

    # Add labels on top of each bar for clarity
    for bars in (bars1, bars2):
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

    # Add a legend
    plt.legend(title='Dataset')

    plt.show()

if __name__ == "__main__":
    ta_files = get_all_file_paths(data_folder="./data/taillard", absolute_paths=True)
    dmu_files = get_all_file_paths(data_folder="./data/demirkol", absolute_paths=True)

    print(f"Taillard instances: {ta_files}")
    print(f"Demirkol instances: {dmu_files}")

    ta_job_count = get_nr_of_jobs(ta_files)
    dmu_job_count = get_nr_of_jobs(dmu_files)

    '''
    plot_counts(ta_job_count, x_label="Job Count", 
                title="Number of jobs and their occurences.", 
                legend_title='Taillard')

    plot_counts(dmu_job_count, x_label="Job Count", 
                title="Number of jobs and their occurences.", 
                legend_title='Demirkol')
    '''
    plot_side_by_side_counts(ta_job_count, 
                             dmu_job_count, 
                             legend_titles=['Taillard', 'Demirkol'], 
                             title='Taillard vs Demirkol: Nr of Jobs')