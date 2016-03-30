#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    :copyright:     (c) 2016 by Alvaro Soto
    :license:       GPL v3, see LICENSE for more details.
    :contact info:  http://headup.ws / alsotoes@gmail.com
"""


import rados
import sys
import subprocess
import re


# http://stackoverflow.com/questions/1094841/
def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def size_per_pool(sizes, pool):
    try:
        p_ls = subprocess.Popen("/usr/bin/rbd --pool " + pool + " ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p_ls.stdout.readlines():
            p_info = subprocess.Popen("/usr/bin/rbd --pool " + pool + " info " + line.strip() + " | /bin/grep size", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for info in p_info.stdout.readlines():
                size = info.strip()
                size = re.sub(r'size\w*\s*', "", size)
                size = re.split('\s+', size)
                sizes[size[1]] += int(size[0])
            retval = p_info.wait()
        retval = p_ls.wait()
    except subprocess.CalledProcessError as e:
        print e.output


def calculate_by_pool(cluster, sizes):
    pools = cluster.list_pools()
    for pool in pools:
        #print pool
        size_per_pool(sizes, pool)


def adjust_values(sizes):
    sizes["GB"] += sizes["TB"] * 1024
    sizes["MB"] += sizes["GB"] * 1024
    sizes["kB"] += sizes["MB"] * 1024
    sizes["bytes"] += sizes["kB"] * 1024


def main():
    sizes = dict()

    cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
    cluster.connect()

    sizes = {"bytes": 0, "kB": 0, "MB": 0, "GB": 0, "TB": 0}

    print "==============="
    print "Provisioned space (all pools, not cephfs): ",
    calculate_by_pool(cluster, sizes)
    adjust_values(sizes)
    print sizeof_fmt(sizes["bytes"])
    print "==============="


# Start program
if __name__ == "__main__":
    main()
