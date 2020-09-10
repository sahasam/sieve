"""
filters.py

Usage:
sieve -r <regex> -o <path>
sieve -i <file> [-ds]

-r <regex>, --regex <regex>         regex expression to match encoding
-o <path>, --output <path>          destination folder for regex exp [default: ./filtered]
-i <file>, --input <file>           file with regex expression and destination folders
-d, --daemon                        run in the background
-s, --startup                       run command on startup (implies daemon)
"""
import os
import re
import sys
import threading

from docopt import docopt

import sieve.utils.utils

#simple filter which does nothing more than
#change directory
class BaseFilter :
    def __init__ (self, target_dir, regex, output_dir):
        self.target_dir = target_dir
        self.regex = regex
        self.output_dir = output_dir

        self.verifyInputs()

    def execute (self):
        dir_list = os.listdir(self.target_dir)
        r = re.compile(self.regex)
        matches = list(filter(r.match, dir_list))

        for match in matches :
            os.replace(f"{self.target_dir}{match}", f"{self.output_dir}{match}")


#deals with large folders to filter (>50 files)
class MultithreadedFilter (BaseFilter) :
    def __init__ (self, regex, output):
        super.__init__(regex, output)


#class to read input file and create necessary
# filters
class FilterConfig :
    def __init__ ():
        print("Under Construction")


def singleFilter () :
    argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)

    bf = BaseFilter(target_dir="./", regex=".*\.txt", output_dir="./output/")
    bf.execute()

def fileFilter () :
    argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)

    print ("filtering from file")