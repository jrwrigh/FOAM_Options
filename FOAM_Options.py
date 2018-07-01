import PyFoam
import re
import subprocess
from pathlib import Path

#####################
# Inputs------------
casepath = Path(
    '~/OpenFOAM/u2berggeist-v1712/run/tutorials/incompressible/icoFoam/cavity/cavity'
)

# /Inputs-------------
########################

# Equivalent of running `. ~/OpenFOAM/OpenFOAM-v1712/etc/bashrc
# && icoFoam -case ~/OpenFOAM/u2berggeist-v1712/run/tutorials/incompressible/icoFoam/cavity/cavity`
# in a new terminal
def getErrorOut(casepath):
    termout = subprocess.run(
        [
            '. ~/OpenFOAM/OpenFOAM-v1712/etc/bashrc && icoFoam -case {}'.format(
                casepath.as_posix())
        ],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).stdout.decode('utf-8')



