#!/usr/bin/env python3

import os
import sys
import argparse

def percent_to_graph(percent, total_length=20):
    """
    Converts a percentage value into a string with hash symbols representing a bar graph.
    
    Args:
    percent (float): Percentage value between 0.0 and 1.0.
    total_length (int): Length of the bar graph, default is 20.
    
    Returns:
    str: A bar graph representation of the percentage.
    """
    hash_count = int(percent * total_length)  # Number of hashes
    return '#' * hash_count + ' ' * (total_length - hash_count)

print (percent_to_graph(0.62))

def get_sys_mem():
    """
    Retrieves the total system memory from /proc/meminfo.
    
    Returns:
    int: Total memory in kilobytes (kiB).
    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal'):
                return int(line.split()[1])  # Return the value in kilobytes
print (get_sys_mem())  # it will display kilobytes

def get_avail_mem():
    """
    Retrieves the available system memory from /proc/meminfo.
    
    Returns:
    int: Available memory in kilobytes (kiB).
    """
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemAvailable'):
                return int(line.split()[1])  # Return the value in kilobytes
print (get_avail_mem())  # Should return available system memory in kilobytes.
