#!/usr/bin/env python
#
# Configuration script to setup
# environment for Effective Hessian code compilation
#
# Intent of this script is to parse flags and arguments
# for storing user's choice of compilers and libraries
#
# Written by Vsevolod D. Dergachev
# University of Nevada, Reno, January 2020

import os
import sys
import getpass
import socket
from datetime import datetime
from argparse import ArgumentParser

def parse_argument_list():

    parser = ArgumentParser(description = "Setup environment for Effective Hessian operation")
    group = parser.add_argument_group('Compiler')
    group.add_argument('--fc',
           action='store',
           default='gfortran',
           help='Your choice of Fortran compiler [default: gfortran]',
           metavar='STRING')
    group.add_argument('--fcflags',
           action='store',
           default='-O0 -g -fcheck=bounds -fcheck=all -C',
           help='FC flags [default: -O0 -g -fcheck=bounds -fcheck=all -C]',
           metavar='STRING')
   
    group = parser.add_argument_group('Choice of math library')
    group.add_argument('--lib_path',
           action='store',
           default='/usr/local/include/mkl/lib/intel64',
           help='Absolute path to math library \
           [default: /usr/local/include/mkl/lib/intel64]',
           metavar='STRING')
    group.add_argument('--libs',
           action='store',
           default='-lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl',
           help='Add on requested libraries',
           metavar='STRING')

    return parser.parse_args()

def main(argv):
 
 pyth_version = sys.version

 if pyth_version < '2.4':
         print('Configuration requires Python version >=2.4')
         sys.exit(1)

 user = getpass.getuser()
 host = socket.gethostname()
 date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

 comp_directory = os.path.dirname(os.path.realpath(__file__))
 log_file = os.path.relpath('Makefile',comp_directory)
 
 args = parse_argument_list()
 
 with open(log_file, 'w') as f:
     f.write('# This Makefile is automatically generated by configure script\n\
# located at: {0}\n\
# time: {1}\n\
# user: {2}\n\
# host: {3}\n\
# Do not edit this file (or do with care if professional)\n\
# At least, re-configure is preferred over editing\n'.format(comp_directory,date_and_time,user,host))
 f.close()
 with open(log_file, 'a+') as f:
     f.write('\nvpath %.f90 source\n\
\nFC = {0}\n\
FCFLAGS = {1}\n\
MKL = -L{2}\n'.format(args.fc,args.fcflags,args.lib_path))
 f.close()
 with open(log_file,'a+') as f:
     f.write("\neff_obj = constants.o ams.o \
readinput.o strings.o\\\n\
           rdGAMESS.o rdMolpro.o normal_mode.o vib.o write.o driver.o main.o \
\n\neffhess : $(eff_obj)\n\
\t$(FC) $(FCFLAGS) -o effhess.x $^ $(MKL) {0}\n".format(args.libs))
 f.close()
 with open(log_file,'a+') as f:
     f.write("\n%.o : %.f90\n\t$(FC) $(FCFLAGS) -c $^\n\
\n%.o : %.f\n\t$(FC) $(FCFLAGS) -c $^\n\
\n.PHONY: cleanall clean\n\
\ncleanall:\n\t-rm -f *.o *.mod\n\
\t-rm -f effhess.x\n\
\nclean:\n\t-rm -f *.o *.mod\n\
")
 f.close()
  
if __name__ == '__main__':
    main(sys.argv)