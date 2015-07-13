#!/usr/bin/env python

import subprocess
import sys, os
import datetime
from pprint import pprint


CMD = '/usr/bin/iostat -dxy 5 1'.split()
HEADER = "Device:      rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util"
FIELD_NAMES = HEADER.split()
EPOCH = datetime.datetime(1970, 1, 1)


def run_process(exe):    
    os.environ['LC_ALL'] = 'en_US.utf8'
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        retcode = p.poll() #returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if not retcode is None:
            break


def get_metrics():
    metrics = {}
    for line in run_process(CMD):
        stats = line.split()
        if len(stats) and stats[0].startswith('sd'):
            device_name = stats[0]
            for idx in xrange(1, len(FIELD_NAMES)): # No device name
                metrics[device_name + ' ' + FIELD_NAMES[idx]] = stats[idx]
    # Here we have matrix of metrics :-)
    pprint(metrics)
    return metrics


def print_metrics(metrics, stats):
    metrics_to_print = []
    for key in metrics.keys():
        for stat in stats:
            if stat in key:
                metrics_to_print.append(metrics[key])
    metrics_to_print.sort()
    print([metrics[stat] for stat in metrics_to_print])


def main():
    while True:
        try:
            stats_to_collect = ['util', 'kB/s']
            metrics = get_metrics()
            print_metrics(metrics, stats_to_collect)
        except KeyboardInterrupt:
            exit()

"""
1. Get all lines
2. Get header of requested stats
2. If header not printed, print it
2. Create list all device_metrics
3. Print only those requested
"""

if __name__ == "__main__":
    main()
