#!/usr/bin/env python3

import csv
import io
import logging
import sys
from datetime import datetime

import dateutil.tz

# CSV column names. Used to create a header row.
FIELDNAMES = ['Timestamp', 'Address', 'ZIP', 'FullName', 'FooDuration',
              'BarDuration', 'TotalDuration', 'Notes']


def norm_timestamp(timestamp):
    dt = datetime.strptime(timestamp, '%m/%d/%y %I:%M:%S %p')
    dt.replace(tzinfo=dateutil.tz.gettz('US/Pacific'))
    eastern = dt.astimezone(dateutil.tz.gettz('US/Eastern'))
    return eastern.isoformat()


def norm_zipcode(zipcode):
    padding = '0' * (5 - len(zipcode))
    return padding + zipcode


def norm_name(name):
    return name.upper()


def norm_duration(duration):
    (h, m, ss) = duration.split(":")
    (s, ms) = ss.split(".")
    seconds = float(h) * 60 * 60 + float(m) * 60 + float(s) + float(ms) / 1000
    return seconds


def normalize_csv(csv_file, out=sys.stdout):
    """Normalizes a CSV file and outputs it to 'out' stream.

    Arguments:
    csv_file -- a file object with the CSV to normalize; must be UTF-8 encoded

    Keyword arguments:
    out -- the stream to which to output the normalized CSV; must be UTF-8
           encoded (defaults to sys.stdout)
    """
    reader = csv.DictReader(csv_file)
    writer = csv.DictWriter(out, fieldnames=FIELDNAMES)
    writer.writeheader()
    for row in reader:
        try:
            row['Timestamp'] = norm_timestamp(row['Timestamp'])
            row['ZIP'] = norm_zipcode(row['ZIP'])
            row['FullName'] = norm_name(row['FullName'])
            row['FooDuration'] = norm_duration(row['FooDuration'])
            row['BarDuration'] = norm_duration(row['BarDuration'])
            row['TotalDuration'] = row['FooDuration'] + row['BarDuration']

            writer.writerow(row)
        except Exception as e:
            logging.error("Unexpected format in row. Error: {}".format(e))
            logging.error("Skipping row: {}".format(row))


if __name__ == "__main__":
    # Replace unicode errors in stdin with U+FFFD. For details, see:
    # https://docs.python.org/3/library/codecs.html#error-handlers
    wrap_stdin = io.TextIOWrapper(
        sys.stdin.buffer, encoding='utf-8', errors='replace')

    # On many modern systems, stdout is already utf-8 encoded, so we don't need
    # to provide anything extra to the normalize_csv call. To be on the safe
    # side for the rare system that might not default to utf-8, here we
    # reconfigure our stdout before calling normalize_csv():
    sys.stdout.reconfigure(encoding='utf-8')
    normalize_csv(wrap_stdin)
