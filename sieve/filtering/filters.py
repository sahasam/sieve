import os
import re
import sys
import threading
import time

from docopt import docopt

POLL_DELAY = 5 #seconds

#simple filter which does nothing more than
#change directory
class BaseFilter :
    def __init__(self, target_dir, regex=None, output_dir=None, rule=[None, None]) :
        self.target_dir = target_dir
        self.regex = regex if regex is not None else rule[0]
        self.output_dir = output_dir if output_dir is not None else rule[1]

        self.regex = self._verify_inputs()

    def execute(self):
        #create a list of matching filenames
        dir_list = os.listdir(self.target_dir)
        matches = list(filter(self.regex.match, dir_list))

        #move every detected match
        for match in matches :
            os.replace(os.path.join(self.target_dir, match),
                os.path.join(self.output_dir, match))
    
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
    def __init__(self, input_file, target_dir) :
        self.input_file = input_file
        self.target_dir = target_dir
        self.filters = []

        self._parse_input_file()
  
    def _parse_input_file(self) :
        #very simple parser. Good enough for now. Make more
        #robust later.
        with open(os.path.join(self.target_dir, self.input_file)) as fp :
            cnt = 0
            for line in fp:
                if line.startswith(';') :
                    continue                # line is a comment and should be ignored
                
                tokens = line.split()
                if len(tokens) != 2 :
                    continue                # incorrect amount of arguments. Ignored
                
                try: 
                    comp_re = self._verify_inputs(regex=tokens[0], output_dir=tokens[1])
                    self.filters.append([comp_re, tokens[1]])
                except Exception as e:
                    print("Failed to verify inputs. Skipping")
                
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

        return comp_re
    
    def execute(self) :
        for rule in self.filters :
            bf = BaseFilter(self.target_dir, rule=rule)
            bf.execute()



#TODO : FIX THIS LUDRICROUS CODE
class BackgroundHandler :
    def __init__ (self, target_dir, input_file) :
        self.target_dir = target_dir
        self.input_file = input_file

        #get list of BaseFilters for every regex pattern and output_dir combo
        ff = FileFilter(input_file, target_dir)
        ff.execute()
        self.filters = ff.filters

    def execute(self) :
        try:
            while True :
                time.sleep(POLL_DELAY)
                #poll directory for matches
                dir_list = os.listdir(self.target_dir)
                matches = []
                for rule in self.filters :
                    matches = list(filter(rule[0].match, dir_list))

                    #move every detected match
                    for match in matches :
                        os.replace(os.path.join(self.target_dir, match),
                            os.path.join(rule[1], match))

                #move matches
        except KeyboardInterrupt :
            exit(1)

    def _on_detected(self, event) :
        print("detected a file: ", event.src_path)
        filename = event.src_path.split('/')[-1]
        output_dir = ""
        for rule in self.filters :
            if rule[0].match(filename) :
                output_dir = rule[1]
        
        os.replace(f"{event.src_path}",
            os.path.join(output_dir, event.src_path.split('/')[-1]))



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


def singleFilter(args) :
    bf = BaseFilter(target_dir="./",
        regex=args['--regex'],
        output_dir=args['--output'])
    bf.execute()

def daemonFilter(args) :
    bh = BackgroundHandler(target_dir="./",
        input_file=args['--input'])
    bh.execute()

def fileFilter(args) :
    ff = FileFilter(input_file=args['--input'],
        target_dir="./")

    ff.execute()