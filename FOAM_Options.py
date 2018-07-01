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
listregex = re.compile(r'^\(\n(.*)\)$', re.MULTILINE | re.DOTALL)


def getErrorOut(casepath):
    """ Get the STDERR from icoFoam """
    termout = subprocess.run(
        [
            '. ~/OpenFOAM/OpenFOAM-v1712/etc/bashrc && icoFoam -case {}'.
            format(casepath.as_posix())
        ],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).stdout.decode('utf-8')

    return (termout)


def parseErrorOut(termout):
    """ Parse terminal output, return option list"""

    output = listregex.search(termout).group(1).splitlines()
    return (output)


##################
# TEST SECTION------

termout = getErrorOut(casepath)
output = parseErrorOut(termout)
