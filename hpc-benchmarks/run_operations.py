import subprocess
from dotenv import load_dotenv
import os
import csv

from extract_tflops import extract_tflops, scan_for_file, delete_files


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')


def generate_and_run_combinations():
    load_dotenv()

    threads = [int(os.getenv('THREADS_MIN')), int(os.getenv('THREADS_MED')), int(os.getenv('THREADS_MAX'))]
    processes = [int(os.getenv('PROCESSES_MIN')), int(os.getenv('PROCESSES_MED')), int(os.getenv('PROCESSES_MAX'))]
    exec_command = os.getenv('EXEC_COMMAND')
    matrix_sizes = [int(os.getenv('MATRIX_SIZE_MIN')), int(os.getenv('MATRIX_SIZE_MED')),
                    int(os.getenv('MATRIX_SIZE_MAX'))]
    block_sizes = [int(os.getenv('BLOCK_SIZE_MIN')), int(os.getenv('BLOCK_SIZE_MED')), int(os.getenv('BLOCK_SIZE_MAX'))]
    parameter_1 = int(os.getenv('PARAMETER_1'))
    flags = os.getenv('FLAGS').split()

    all_combinations = [(num_threads, num_processes, static_matrix_size, static_block_size)
                        for num_threads in threads
                        for num_processes in processes
                        for static_matrix_size, static_block_size in zip(matrix_sizes, block_sizes)]

    csv_file_path = 'tflops_results.csv'

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        header = ['Num Threads', 'Num Processes', 'Matrix Size', 'Block Size', 'Parameter 1', 'TFLOPS']
        csv_writer.writerow(header)

        for num_threads, num_processes, matrix_size, block_size in all_combinations:
            command = f'OMP_NUM_THREADS={num_threads} mpirun -n {num_processes} {exec_command} {matrix_size} {block_size} {parameter_1} {" ".join(flags)}'
            print(f"Running command: {command}")
            return_code, stdout, stderr = run_command(command)
            print(f"Return Code: {return_code}")
            print(f"Standard Output:\n{stdout}")
            print(f"Standard Error:\n{stderr}")
            print("\n" + "=" * 50 + "\n")
            tflops = extract_tflops(scan_for_file(), f'{num_threads}_{num_processes}_{matrix_size}_{block_size}_{parameter_1}')

            row = [num_threads, num_processes, matrix_size, block_size, parameter_1, tflops]
            csv_writer.writerow(row)

    delete_files()


if __name__ == "__main__":
    generate_and_run_combinations()
