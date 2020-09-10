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
    def __init__(self, target_dir, regex, output_dir) :
        self.target_dir = target_dir
        self.regex = regex
        self.output_dir = output_dir

        self.regex = self.verifyInputs()

    def execute (self):
        dir_list = os.listdir(self.target_dir)
        matches = list(filter(self.regex.match, dir_list))

        for match in matches :
            os.replace(f"{self.target_dir}{match}",
                f"{self.output_dir}{match}")
    
    def verifyInputs(self) :
        #target_dir must be a valid directory and end in '/'
        valid_target = os.path.isdir(self.target_dir)
        if not valid_target :
            raise InputError(self.target_dir,
                f"{self.target_dir} is not a directory")
 
        #output_dir must be a valid directory and end in '/'
        valid_output = os.path.isdir(self.output_dir)
        if not valid_output :
            raise InputError(self.output_dir,
                f"{self.output_dir} is not a directory")

        #regex must be valid
        try:
            comp_re = re.compile(self.regex)
        except re.error as e:
            raise

        return comp_re


#deals with large folders to filter (>50 files)
class MultithreadedFilter (BaseFilter) :
    def __init__ (self, regex, output):
        super.__init__(regex, output)


#class to read input file and create necessary
# filters
class FilterConfig :
    def __init__ ():
        print("Under Construction")

class InputError(Exception) :
    """Exception raised for errors in the input

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of error
    """
    def __init__(self, expression, message) :
        self.expression = expression
        self.message = message
        super().__init__(message)


def singleFilter () :
    argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)

    bf = BaseFilter(target_dir="./",
                    regex=args['--regex'],
                    output_dir=args['--output'])
    bf.execute()

def fileFilter () :
    argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)

    print ("filtering from file")