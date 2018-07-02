import PyFoam
import re
import subprocess
from pathlib import Path
from functools import reduce
import json

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


def changeDictionary(dictionary, path, newvalue):
    """ Changes value of the given dictionary """
    if not isinstance(path, str) and len(path) > 1:
        reduce(dict.__getitem__, path[:-1], dictionary)[path[-1]] = newvalue
    elif type(path) is str:
        dictionary[path] = newvalue


def makeJSON(dictionary, filepath):
    """ Save dictionary to JSON file"""
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    with filepath.open('w') as jsonfile:
        json.dump(dictionary, jsonfile)


##################
# TEST SECTION------

termout = getErrorOut(casepath)
output = parseErrorOut(termout)
