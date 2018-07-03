# FOAM_Options

This is a Python based script to get a list of the available options for a given setting located in a OpenFOAM dictionary. This was originally done in support of [vim-foam](https://github.com/lervag/vim-foam).

# Overview
This script works by using the error message that comes with a misspelled error to get a list of the available options for a key in OpenFOAM dictionaries. It works

1. Change the OpenFOAM dictionary entry to something wrong
2. Run the solver (currently hardcoded to `icoFoam`) and collect the error message
3. Parse the error message for the list of correct options
4. Add that list to a dictionary
5. Replace the old entry to the OpenFOAM dictionary (ie. the correct entry)
6. Repeat

# How to Use?
See `example.py` for a full example with logging. The main function to use is `loopFOAMOptions()` which takes in `casepath`, `FOAMDictionarypath`, and `ChangesList`.

`casepath` is simply the filepath to the case that will be used for the error parsing purposes (see step 2 in [Overview](#overview)). This can be a string or a `pathlib.Path` object. 

`FOAMDictionarypath` is simply the path to the dictionary file to be changed (see step 1 and 5 in [Overview](#overview)). This can be a string or a `pathlib.Path` object. It can also be simply the name of the dictionary (ie. `fvSchemes` or `controlDict`). This will be automatically assumed to be in the `casepath` file path under `/system/[DICTIONARY NAME]`. See the `interpretFOAMDictionarypath()` function for more details.

`ChangesList` is the list of changes to be made to the dictionary (see step 1 and 5 in [Overview](#overview)). It is given as a tuple of `keypath` and `newvalue`, where `keypath` is the path to get to the value to be changed and `newvalue` is the newvalue to be assigned to said value.
As most OpenFOAM dictionaries are nested, the `keypath` to get to the desired value must be given as as tuple of strings. For example, if I wanted to edit the ddtSchemes default options, then `keypath = ('ddtSchemes', 'default')`. See `example.py` for more examples of this.
