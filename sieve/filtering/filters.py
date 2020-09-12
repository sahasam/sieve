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
import time

from docopt import docopt
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

#simple filter which does nothing more than
#change directory
class BaseFilter :
    def __init__(self, target_dir, regex, output_dir) :
        self.target_dir = target_dir
        self.regex = regex
        self.output_dir = output_dir

        self.regex = self._verifyInputs()

    def execute (self):
        dir_list = os.listdir(self.target_dir)
        matches = list(filter(self.regex.match, dir_list))

        for match in matches :
            os.replace(f"{self.target_dir}{match}",
                f"{self.output_dir}{match}")
    
    def _verifyInputs(self) :
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

class FileFilter :
    def __init__ (input_file, target_dir) :
        print("hello world")

class BackgroundHandler :
    def __init__ (self, target_dir, regex, output_dir) :
        self.target_dir = target_dir
        self.regex = regex
        self.output_dir = output_dir

        #get list of BaseFilters for every regex pattern and output_dir combo
        
        ehandler = RegexMatchingEventHandler(regexes=[f"{self.regex}"],
            ignore_regexes=[],
            ignore_directories=True,
            case_sensitive=True)
        ehandler.on_modified = self._on_detected
        ehandler.on_created = self._on_detected

        observer = Observer()
        observer.schedule(event_handler=ehandler, path=target_dir)
        observer.start()

        try:
            while True :
                time.sleep(1)
        except KeyboardInterrupt :
            observer.stop()
        
        observer.join()

    
    def _on_detected(self, event) :
        print(event.src_path, event.src_path.split('/')[-1])
        os.replace(f"{event.src_path}",
            f"{self.output_dir}{event.src_path.split('/')[-1]}")

#class to read input file and create necessary
# filters
class FilterConfig :
    def __init__ (inFile='./filters.txt') :
        self.inFile = inputFile

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


def singleFilter (args) :
    bf = BaseFilter(target_dir="./",
        regex=args['--regex'],
        output_dir=args['--output'])
    bf.execute()

def daemonFilter (args) :
    bh = BackgroundHandler(target_dir="/Users/sahasmunamala/dev/sieve",
        regex=args['--regex'],
        output_dir=args['--output'])

def fileFilter () :
    argv = sys.argv[1:]
    args = docopt(__doc__, argv=argv)

    print ("filtering from file")