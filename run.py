#!/usr/bin/python

import sys
import os
import subprocess
import importlib
import argparse
from time import *
from machinekit import launcher

launcher.register_exit_handler()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser(description='This is the CRAMPS2 run script '
                                 'it demonstrates how a run script could look like '
                                 'and of course starts the CRAMPS2 config')

parser.add_argument('-v', '--video', help='Starts the video server', action='store_true')
parser.add_argument('-d', '--debug', help='debug level', type=int, choices=[0 , 1, 2, 3, 4, 5])

args = parser.parse_args()

try:
    launcher.check_installation()                                     # make sure the Machinekit installation is sane
    launcher.cleanup_session()                                        # cleanup a previous session

    # set debug level
    if args.debug:
        launcher.set_debug_level(args.debug)


    launcher.load_bbio_file('cramps.bbio')                    # load a BBB universal overlay
    #launcher.install_comp('thermistor_check.comp')
    #launcher.install_comp('gantry.comp')                      # install a comp HAL component of not already installed
    launcher.start_process('configserver -d -n RIGIDBOT ~/ui')   # start the configserver

#    if args.video:
#        launcher.start_process('videoserver --ini video.ini Webcam1')

    launcher.start_process('machinekit -vd CRAMPS.ini')                        # start linuxcnc

except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

while True:
    sleep(1)
    print('here')
    launcher.check_processes()

