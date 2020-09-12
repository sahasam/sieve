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

        self.regex = self._verify_inputs()

    def execute (self):
        #create a list of matching filenames
        dir_list = os.listdir(self.target_dir)
        matches = list(filter(self.regex.match, dir_list))

        #move every detected match
        for match in matches :
            os.replace(f"{self.target_dir}{match}",
                f"{self.output_dir}{match}")
    
    def _verify_inputs(self) :
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

        return comp_re                      # return the compiled regex for convenience



class FileFilter :
    def __init__ (self, input_file, target_dir) :
        self.input_file = input_file
        self.target_dir = target_dir
        self.filters = []

        self._parse_input_file()
  
    def _parse_input_file(self) :
        #very simple parser. Good enough for now. Make more
        #robust later.
        with open(os.path.join(self.target_dir, self.input_file)) as fp:
            cnt = 0
            for line in fp:
                if(line.startswith(';')) :
                    continue                # line is a comment and should be ignored
                
                tokens = line.split()
                if len(tokens) != 2 :
                    continue                # incorrect amount of arguments. Ignored
                
                if self._verify_inputs(regex=tokens[0], output_dir=tokens[1]) :
                    self.filters.append((tokens[0], tokens[1]))
    
    def _verify_inputs(self, regex, output_dir) :
        #verify regex is valid
        try:
            comp_re = re.compile(regex)
        except re.error as e:
            raise

        #verify output directory is a real directory
        if not os.path.isdir(output_dir) :
            raise InputError(output_dir,
                f"{output_dir} is not a directory")
        
        return True


class BackgroundHandler :
    def __init__ (self, target_dir, input_file, output_dir) :
        self.target_dir = target_dir
        self.input_file = input_file
        self.output_dir = output_dir

        #get list of BaseFilters for every regex pattern and output_dir combo
        ff = FileFilter(input_file, target_dir)
        regex_list = [ff.filters[0][0]]
        
        ehandler = RegexMatchingEventHandler(regexes=regex_list,
            ignore_regexes=['filters\.txt'],
            ignore_directories=True,
            case_sensitive=True)
        ehandler.on_modified = self._on_detected
        ehandler.on_created = self._on_detected

        observer = Observer()
        observer.schedule(event_handler=ehandler, path=target_dir)
        observer.start()

        #TODO : FIX THIS LUDRICROUS CODE
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
        input_file="/Users/sahasmunamala/dev/sieve/filters.txt",
        output_dir="/Users/sahasmunamala/dev/sieve/output/")