#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    :copyright:     (c) 2015 by Alvaro Soto
    :license:       GPL v2, see LICENSE for more details.
    :contact info:  http://headup.ws / alsotoes@gmail.com
"""

import argparse
import textwrap
import rados
import math
import sys
import csv
import re
import os


# http://stackoverflow.com/questions/1094841/
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def args_parse():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                ===============
                Connect to local ceph cluster to get available and total space.
                    * Works only locally reading ceph.conf.
                    * Uses a ratio to set working storage space on calculations.
                ===============
            '''))

    parser.add_argument("--config", type=str, default="/etc/ceph/ceph.conf", help='Ceph config file (ceph.conf).')
    parser.add_argument("--ratio", type=float, default=0.2, help='Reserved storage ratio, by default 0.2 as a 20%%.')
    parser.add_argument("--output", type=str, required=False, choices=["csv", "txt"], help='Output format to print in stdout.')
    parser.add_argument("--file", type=str, required=False, help='Output CSV file, this option override --output.')
    parser.add_argument("name", type=str, help='Cluster fancy name.')

    return parser.parse_args()


def print_txt(ceph):
    print "==============="
    print "Cluster codename: " + ceph['name']
    print "Cluster ID: " + ceph['fsid']
    print "Cluster mon to connect: " + ceph['mon']
    print "Cluster Statistics"

    print "\tTotal: " + sizeof_fmt(ceph['total'] * 1024)
    print "\tReserved: " + sizeof_fmt(ceph['reserved'] * 1024)
    print "\tUsable (before warning): " + sizeof_fmt(ceph['usable'] * 1024)
    print "\tUsed: " + sizeof_fmt(ceph['used'] * 1024)
    print "\n"
    print "\tTotal Available: " + sizeof_fmt(ceph['available'] * 1024)
    print "\tPercentage Available: " + str(ceph['p_available']) + "%"
    print "==============="


def print_csv(ceph, filename, let):
    f = open(filename+".csv", 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow(["Cluster Name", "Cluster ID", "Cluster MON", "Total", "Reserved", "Usable", "Used", "Available", "Percentage Available"])
        writer.writerow([ceph['name'], ceph['fsid'], ceph['mon'], sizeof_fmt(ceph['total'] * 1024),
            sizeof_fmt(ceph['reserved'] * 1024), sizeof_fmt(ceph['usable'] * 1024),
            sizeof_fmt(ceph['used'] * 1024), sizeof_fmt(ceph['available'] * 1024),
            str(ceph['p_available']) + "%"])
    finally:
        f.close()

    print open(filename+".csv", 'rt').read()
    
    if not let:
        os.remove(filename+".csv")

def get_cluster_info(cluster, ceph):
    ceph['default_size'] = int(cluster.conf_get('osd pool default size'))
    ceph['mon'] = cluster.conf_get('mon initial members')
    ceph['fsid'] = cluster.get_fsid()

    return cluster.get_cluster_stats()


def get_and_calculate(cluster_stats, ceph, args):
    ceph['name'] = args.name
    ceph['reserved_ratio'] = float(args.ratio)
    ceph['total'] = long(cluster_stats['kb']) / ceph['default_size']
    ceph['reserved'] = long(cluster_stats['kb'] * (ceph['reserved_ratio'])) / ceph['default_size']
    ceph['usable'] = long(cluster_stats['kb'] * (1 - ceph['reserved_ratio'])) / ceph['default_size']
    ceph['used'] = long(cluster_stats['kb_used']) / ceph['default_size']
    ceph['available'] = ceph['usable'] - ceph['used']
    ceph['p_available'] = (ceph['available'] * 100) / ceph['usable']


def main():
    ceph = dict()
    args = args_parse()

    cluster = rados.Rados(conffile=args.config)
    cluster.connect()

    cluster_stats = get_cluster_info(cluster, ceph)
    get_and_calculate(cluster_stats, ceph, args)

    if not args.output:
        args.output = "txt"

    if not args.file:
        args.file = "output"
        let = 0
    else:
        let = 1

    print_txt(ceph) if "txt" == args.output else print_csv(ceph, re.sub('[^0-9a-zA-Z]+', '_', args.file), let)


# Start program
if __name__ == "__main__":
    main()
