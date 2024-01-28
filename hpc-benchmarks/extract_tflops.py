import os
import time


def delete_files():
    files = [file for file in os.listdir() if file.startswith('Timerdump')]
    for file in files:
        os.remove(file)


def scan_for_file():
    while True:
        files = [file for file in os.listdir() if file.startswith('Timerdump')]

        if files:
            latest_file = max(files, key=lambda x: os.path.getmtime(x))
            return latest_file

        time.sleep(1)


def extract_tflops(file, operation):
    with open(file, 'r') as timerdump:
        lines = timerdump.readlines()

    for line in lines:
        if line.startswith('GEMM_TOTAL:'):
            return line.split()[1]
