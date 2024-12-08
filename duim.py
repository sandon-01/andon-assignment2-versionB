#!/usr/bin/env python3

import subprocess
import argparse


'''
OPS445 Assignment 2
Program: duim.py 
Author: Shermalyn Andon
The python code in this file (duim.py) is original work written by
Shermalyn Andon. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or online resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: A tool to display disk usage of directories and their subdirectories with bar graphs representing their sizes.
Date: 12/03/2024
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Print sizes in human-readable format (e.g. 1K, 23M, 2G)")
    parser.add_argument("target", nargs="?", default=".", help="The directory to scan (default is current directory).")
    args = parser.parse_args()
    return args


def percent_to_graph(percent: int, total_chars: int) -> str:
    "returns a string: eg. '##  ' for 50 if total_chars == 4"
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    num_equals = round((percent / 100) * total_chars)
    num_spaces = total_chars - num_equals
    return '=' * num_equals + ' ' * num_spaces


def call_du_sub(location: str) -> list:
    "use subprocess to call `du -d 1 + location`, return raw list"
    command = ['du', '-d', '1', location]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()

    if result.returncode != 0:
        # Handle permission errors gracefully by checking the error message
        error_message = err.decode()
        if "Permission denied" in error_message:
            print(f"Warning: Skipping directories with permission issues in {location}")
        else:
            raise Exception(f"Error calling du: {error_message}")

    # decode the output to string, split by newlines, and strip each line
    return out.decode().strip().split('\n')



def create_dir_dict(raw_dat: list) -> dict:
    "get list from du_sub, return dict {'directory': 0} where 0 is size"
    dir_dict = {}
    for line in raw_dat:
        size, path = line.split('\t')
        dir_dict[path] = int(size)
    return dir_dict


def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result


if __name__ == "__main__":
    args = parse_command_args()

    # Get the target directory (default to current directory if not provided)
    target_dir = args.target
    
    # Call du command to get sizes of subdirectories
    raw_data = call_du_sub(target_dir)
    
    # Create a dictionary with directory sizes
    dir_dict = create_dir_dict(raw_data)
    
    # Calculate the total size of the target directory
    total_size = sum(dir_dict.values())

    # Print the bar graph for each subdirectory
    for subdir, size in dir_dict.items():
        percent = (size / total_size) * 100
        bar_graph = percent_to_graph(percent, args.length)
        
        # Print the human-readable size if -H option is passed
        if args.human_readable:
            size_str = bytes_to_human_r(size)
        else:
            size_str = str(size)
        
        print(f"{percent:3.0f} % [{bar_graph}] {size_str:>7} {subdir}")

    # Print the total size of the directory
    if args.human_readable:
        total_size_str = bytes_to_human_r(total_size)
    else:
        total_size_str = str(total_size)
    
    print(f"Total: {total_size_str}   {target_dir}")
