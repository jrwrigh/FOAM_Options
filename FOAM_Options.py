import PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import re
import subprocess
from pathlib import Path
from functools import reduce
import json

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


def getFOAMOptions(casepath, FOAMdictionarypath, keypath, newvalue):

    FOAMdictionary = ParsedParameterFile(
        FOAMdictionarypath.expanduser().as_posix())
    changeDictionary(FOAMdictionary.content, keypath, newvalue)
    FOAMdictionary.writeFile()

    return (parseErrorOut(getErrorOut(casepath)))

def interpretFOAMdictionarypath(FOAMdictionarypath, casepath):

    if FOAMdictionarypath == 'fvSchemes':
        FOAMdictionarypath = casepath / 'system/fvSchemes'
    elif FOAMdictionarypath == 'fvSolution':
        FOAMdictionarypath = casepath / 'system/fvSolution'
    elif FOAMdictionarypath == 'controlDict':
        FOAMdictionarypath = casepath / 'system/controlDict'

def loopFOAMOptions(casepath, FOAMdictionarypath, OptionsList):


    for Options in OptionsList:
        if len(Options) == 2:
            keypath, newvalue = Options
            if len(keypath) > 1:
                # Creates name with ':' between each sub-key
                name = ":".join(keypath)
            else:
                name = keypath


o

######################
# TEST SECTION------

test = 'getFOAMOptions-external'

if test == 'getFOAMOptions-internal':
    casepath = Path(
        '~/OpenFOAM/u2berggeist-v1712/run/tutorials/incompressible/icoFoam/cavity/cavity'
    )
    FOAMdictionarypath = casepath / 'system/fvSchemes'
    keypath = 'ddtSchemes'
    newvalue = {'default': 'EulerFOO'}

    FOAMdictionary = ParsedParameterFile(
        FOAMdictionarypath.expanduser().as_posix())
    changeDictionary(FOAMdictionary.content, keypath, newvalue)
    FOAMdictionary.writeFile()

    termout = getErrorOut(casepath)
    output = parseErrorOut(termout)

elif test == 'getFOAMOptions-function':
    casepath = Path(
        '~/OpenFOAM/u2berggeist-v1712/run/tutorials/incompressible/icoFoam/cavity/cavity'
    )
    FOAMdictionarypath = casepath / 'system/fvSchemes'
    keypath = 'ddtSchemes'
    newvalue = {'default': 'EulerFOO'}

    output = getFOAMOptions(casepath, FOAMdictionarypath, keypath, newvalue)
