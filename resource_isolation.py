import subprocess

# Function to run a workload inside a container with allocated cache
def run_workload_with_cat(cache_allocation_percentage):
    cat_cmd = f"sudo cset set -s system.slice -l {cache_allocation_percentage}"
    workload_cmd = "your_workload_command_here"  # Replace with the actual workload command

    # Execute the CAT command to allocate cache
    subprocess.run(cat_cmd, shell=True, check=True)

    # Execute the workload inside a container with the allocated cache
    subprocess.run(workload_cmd, shell=True, check=True)

# Example usage: Allocate 25% cache and run the workload
run_workload_with_cat(cache_allocation_percentage=25)
