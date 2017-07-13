#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import argparse
import tempfile
import shutil
import numpy as np
from gro_cutter.walec import get_frames

make_ndx = 'gmx make_ndx -f %s -o %s'
density = 'gmx density -f %s -s %s -n %s -o %s -ng 2'

def parse_xvg(fname):
    ret_arr = np.empty((50, 3), dtype='float32')
    with open(fname) as handle:
        for i, line in enumerate(handle.readlines()[24:]):
            ret_arr[i, :] = line.split()
    return ret_arr


def get_name_and_extension(fpath):
    """

    :param fpath: path to a file
    :return: (name of the file, extension) without directories in the path
    """
    name = os.path.basename(fpath)
    split = name.split('.')
    if len(split) > 1:
        return split
    else:
        return split[0], ''


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='blah') # TODO meaningful description
    parser.add_argument('-i', required=True, help="input file")
    parser.add_argument('-o', required=True, help="output file")
    parser.add_argument('-t', required=True, help='.tpr file')
    args = parser.parse_args(args)
    temp_dir = tempfile.mkdtemp()
    for i, frame in enumerate(get_frames(args.i)):
        base, extension = get_name_and_extension(args.i)
        extension = extension or 'gro'
        temp_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.'+extension))
        index_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.ndx'))
        out_part_name = os.path.join(os.path.join(temp_dir, base+'_'+str(i)+'.xvg'))
        open(temp_name, 'w').write(frame)
        p = subprocess.Popen(make_ndx%(temp_name, index_name), stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE, shell=True)
        p.stdin.write("13 & a P O12 O13 O14\n")
        p.stdin.write("q\n")
        p.wait()
        p = subprocess.Popen(density%(temp_name, args.t, index_name, out_part_name), stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        p.stdin.write("15\n")
        p.stdin.write("14\n")
        p.wait()
        os.remove(temp_name)
        os.remove(index_name)
    arr = []
    for f in os.listdir(temp_dir):
        arr.append(parse_xvg(os.path.join(temp_dir, f)))
    # https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    # sorted_arr = np.sort(np.concatenate(arr).view('f8,f8,f8'), order=['f1'], axis=0).view(np.float)
    np.savetxt(open(args.o, 'wb'), np.mean(arr, axis=0), fmt='%.6f')
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    import time
    t = time.time()
    main(sys.argv[1:])
    print "Computations performed in", time.time() - t

