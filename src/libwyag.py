import argparse
import configparser
from datetime import datetime
from fnmatch import fnmatch
import hashlib
from math import ceil
import os
import re
import sys
import zlib


try:
    import grp, pwd
except ModuleNotFoundError:
    pass

## important lybraries imported each explained on README

argparser = argparse.ArgumentParser(
    description="Wiener-git its a git clone written on python to understand how it works under the hood :)"
)

argsubparsers = argparser.add_subparsers(title="command", dest="Available commands")


## subparser definitions.
