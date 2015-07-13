#!/usr/bin/env python

from cassandra.cluster import Cluster
import random
import datetime
import os
import json
from pprint import pprint


KEYSPACE = 'casssa'
EPOCH = datetime.datetime(1970, 1, 1)
TEST = False

def get_timestamp():
    now = datetime.datetime.now()
    timestamp_sec = now - EPOCH
    timestamp = int(round(timestamp_sec.total_seconds()*1000))
    return timestamp


def main():
    cluster = Cluster()
    session = cluster.connect('casssa')
    
    metrics = [
        "mapnocc_updates_sent",
        "postgresql_wal_delay",
        "postgresql_buffer_utilization"
    ]
    
    if TEST:
        limit = 1
    else:
        limit = 100000000
    for iter in xrange(limit):
        #timestamp = datetime.datetime.now()
        timestamp = get_timestamp()
        data_to_insert = (timestamp, metrics[random.randint(0,2)], '192.168.0.{}'.format(random.randint(1,10)), random.randint(0,100))
        pprint(data_to_insert)
        session.execute("INSERT INTO data_points (ts, metric, tag, value) VALUES (%s, %s, %s, %s)", data_to_insert)


if __name__ == "__main__":
    main()
