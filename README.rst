.. -*- mode: rst -*-
density_profile
====
This is a simple script creating water and POP3 density profile along given axis from .gro files. The script is intended to be used to
process files obtained with https://github.com/wojciech-galan/gro_cutter

How to use
----------
First make sure that you have Python 2.7, numpy and https://github.com/wojciech-galan/gro_cutter installed. Then simply download the 
density_profile.py script and run it: ::

    python density_profile.py -i INFILE -o OUTFILE -t TPRFILE -d AXIS

where:

- INFILE - path to the input file
- OUTFILE - path to the output file
- TPRFILE - path to the .tpr file
- AXIS - X, Y or Z

Citation
--------

# TODO
