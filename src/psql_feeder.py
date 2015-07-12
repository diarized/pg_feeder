#!/usr/bin/env python

import psycopg2 as psql
import random
import datetime
import os

from psycopg2.extras import register_json
register_json(oid=3802, array_oid=3807)

DBNAME = 'casssa'
USERNAME = 'artur'
EPOCH = datetime.datetime(1970, 1, 1)
TEST = True

def get_timestamp():
    now = datetime.datetime.now()
    timestamp_sec = now - EPOCH
    timestamp = int(round(timestamp_sec.total_seconds()*1000))
    return timestamp


def main():
    pass_file = os.path.dirname(os.path.realpath(__file__)) + "/pg_password.txt"
    try:
        with open(pass_file) as fh:
            password = fh.readline()
    except IOError:
        print("Please create password file 'pg_password.txt'.")
        exit(1)
    connection = psql.connect(dbname=DBNAME, user=USERNAME, password=password)
    cursor = connection.cursor()
    
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
        try:
            #timestamp = datetime.datetime.now()
            timestamp = get_timestamp()
            data_to_insert = psql.extras.Json({"metric": metrics[random.randint(0,2)], "value": random.randint(0,100), "tags": "192.168.0.{}".format(random.randint(1,10))})
            cursor.execute("INSERT INTO data_points VALUES(%s, %s)", (timestamp, data_to_insert))
            if iter % 100000 == 0:
                connection.commit()
        except psql.InternalError, KeyboardInterrupt:
            connection.rollback()
            raise
        finally:
            connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
