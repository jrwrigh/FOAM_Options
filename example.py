from FOAM_Options import *
from pathlib import Path
import logging

logging.basicConfig(filename='FOAM_Options.log', level=logging.INFO)

casepath = Path(
    '~/OpenFOAM/u2berggeist-v1712/run/tutorials/incompressible/icoFoam/cavity/cavity'
)
FOAMdictionarypath = 'fvSchemes'

OptionsList = [(('ddtSchemes', 'default'), 'EulerFoo'),
               (('gradSchemes', 'default'), 'GaussFoo')]

loopoutput = loopFOAMOptions(casepath, FOAMdictionarypath, OptionsList)
