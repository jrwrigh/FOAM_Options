import PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import re
import subprocess
from pathlib import Path
from functools import reduce
import json
import logging

listregex = re.compile(r'^\(\n(.*)\)$', re.MULTILINE | re.DOTALL)


def getDictionaryValue(dictionary, path):
    """ Returns value of Dictionary at the specified path"""
    logging.debug(f"getDictionaryValue(dictionary={dictionary}, path={path})"
    if not isinstance(path, str) and len(path) > 1:
        return (reduce(dict.__getitem__, path, dictionary))
    elif type(path) is str:
        return (dictionary[path])


def changeDictionary(dictionary, path, newvalue):
    """ Changes value of the given dictionary """
    logging.debug(
        f"changeDictionary(dictionary={dictionary}, path={path}, newvalue={newvalue})"
    )
    if not isinstance(path, str) and len(path) > 1:
        reduce(dict.__getitem__, path[:-1], dictionary)[path[-1]] = newvalue
    elif type(path) is str:
        dictionary[path] = newvalue
    logging.debug(f"changeDictionary outputed a new dictionary:\n{dictionary}")


def getFOAMdictionary(FOAMdictionarypath, casepath=None):
    """ Returns FOAMdictionary from path """
    FOAMdictionarypath = interpretFOAMdictionarypath(FOAMdictionarypath,
                                                     casepath)
    return ParsedParameterFile(FOAMdictionarypath.expanduser().as_posix())


def interpretFOAMdictionarypath(FOAMdictionarypath, casepath=None):

    logging.debug(
        f'interpretFOAMdictionarypath(FOAMdictionarypath={FOAMdictionarypath}, casepath={casepath})'
    )

    if FOAMdictionarypath == 'fvSchemes':
        FOAMdictionarypath = casepath / 'system/fvSchemes'
    elif FOAMdictionarypath == 'fvSolution':
        FOAMdictionarypath = casepath / 'system/fvSolution'
    elif FOAMdictionarypath == 'controlDict':
        FOAMdictionarypath = casepath / 'system/controlDict'
    elif isinstance(FOAMdictionarypath, str):
        FOAMdictionarypath = Path(FOAMdictionarypath)
    logging.debug(f"interpretFOAMdictionarypath has outputed {FOAMdictionarypath}")

    return FOAMdictionarypath


def makeJSON(dictionary, filepath):
    """ Save dictionary to JSON file"""
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    with filepath.open('w') as jsonfile:
        json.dump(dictionary, jsonfile)


def getErrorOut(casepath):
    """ Get the STDERR from icoFoam """
    logging.debug(f'getErrorOut(casepath={casepath})')
    termout = subprocess.run(
        [
            f'. ~/OpenFOAM/OpenFOAM-v1712/etc/bashrc && icoFoam -case {casepath.as_posix()}'
        ],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE).stderr.decode('utf-8')

    logging.debug(f"getErrorOut outputed:\n{termout}")

    if not termout:
        logging.warning("The regex didn't have anything to parse")

    return (termout)


def parseErrorOut(termout):
    """ Parse terminal output, return option list"""

    try:
        output = listregex.search(termout).group(1).splitlines()
    except:
        pass
    else:
        return (output)


def getFOAMOptions(casepath, FOAMdictionarypath, keypath, newvalue):

    FOAMdictionary = getFOAMdictionary(FOAMdictionarypath, casepath)

    # Get original dictionary value
    originalvalue = getDictionaryValue(FOAMdictionary.content, keypath)

    changeDictionary(FOAMdictionary.content, keypath, newvalue)
    FOAMdictionary.writeFile()

    try:
        output = parseErrorOut(getErrorOut(casepath))
    finally:
        changeDictionary(FOAMdictionary.content, keypath, originalvalue)
        FOAMdictionary.writeFile()

    return output


def loopFOAMOptions(casepath, FOAMdictionarypath, OptionsList):

    logging.info('Started Looping through FOAM Options.')
    logging.info('Beginning parameters:')
    logging.info(f'casepath: {casepath}')
    logging.info(f'FOAMdictionarypath: {FOAMdictionarypath}')
    FOAMOptionsdict = {}
    for Options in OptionsList:
        logging.info('Started working on OptionsList')
        if len(Options) == 2:
            keypath, newvalue = Options
            if len(keypath) > 1:
                # Creates name with ':' between each sub-key
                name = ":".join(keypath)
            else:
                name = keypath

        FOAMOptionsdict[name] = getFOAMOptions(casepath, FOAMdictionarypath,
                                               keypath, newvalue)
        if FOAMOptionsdict[name] == None:
            logging.warning('The following Options did not output a list:')
            logging.warning(
                f'keypath: {keypath}\nnewvalue: {newvalue}\nname: {name}')

    return FOAMOptionsdict
