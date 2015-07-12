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


def add_stats(metrics, device, statistics):
    dev_stats = [device + '_' + stat for stat in statistics]
    metrics.append(dev_stats)


def get_metrics():
    metrics = []
    for line in run_process(CMD):
        stats = line.split()
        if len(fields) and fields[0].startswith('sd'):
            dev_name = stats[0]
            stats_for_dev = stats[1:]
            add_stats(metrics, dev_name, stats_for_dev)
    return metrics


def get_indexes(stats, metrics):
    idxs = []
    for metric in metrics:
        for stat in stats:
            if stat in metric:
                idxs.append(metrics.index(metric))
    return idxs


def print_metrics(metrics, metrics_idxs):
    print([metrics[idx] for idx in metrics_idxs])


def main():
    while True:
        try:
            metrics = get_metrics()
            stats_to_print = ['util', 'kB/s']
            idxs = get_indexes(stats_to_print, metrics)
            print_metrics(metrics, idxs)
        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    main()
