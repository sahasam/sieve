import os
import re
import sys
import threading
import time

from docopt import docopt
from sieve.utils.utils import create_filter_file

POLL_DELAY = 5 #seconds

class BaseFilter :
    """
    Class that is used to represent a filter for a single rule.

    This class accepts either a single rule as an input. When executed,
    the filter searches the target directory for files matching the regex 
    expression, and moves matches to to the destination folder.

    Attributes:
    target_dir : str
        path to directory that will be filtered
    regex : str
        regex expression used to find matches
    output_dir : str
        path to directory that matches will be put into
    
    Methods:
    execute() :
        executes the filter rule once
    """

    def __init__(self, target_dir, regex=None, output_dir=None, rule=[None, None]) :
        """
        Parameters:
        regex : str
            regex pattern used to find matches
        output_dir : str
            path to directory that matches will be put into
        rule : tuple
            tuple containing the regex expression and the output directory
            in that order
        """

        self.target_dir = target_dir
        self.regex = regex if regex is not None else rule[0]
        self.output_dir = output_dir if output_dir is not None else rule[1]

        self.regex = self._verify_inputs()

    def execute(self):
        """Executes the filter rule once."""

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

        # return the compiled regex for convenience
        return comp_re



class FileFilter :
    """
    Class that represents a filter for a .txt file of rules

    This class excepts a file as an input, and parses the text inside of it.
    If rules are found, then they are represented as a tuple and placed in 
    the self.filters list.

    Attributes:
    input_file : str
        name of the file that holds the filter rules. Defaults to "filters.txt"
    target_dir : str
        path to directory that holds filters.txt and where filtering will happen 
    filters : list
        list of filter rules. Stored as a tuple of (regex, destination folder)

    Methods:
    execute()
        executes all the filter rules in the file once.
    """

    def __init__(self, input_file='filters.txt', target_dir) :
        """
        Parameters:

        input_file : str
            name of the file that holds the filter rules. Defaults to "filters.txt"
        target_dir : str
            path to directory that holds filters.txt and where filtering will happen
        """

        self.input_file = input_file
        self.target_dir = target_dir
        self.filters = []

        self._parse_input_file()
  
    def _parse_input_file(self) :
        """Parse the input file in the target directory to extract rules."""
        
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
                except re.error as e:
                    print("Failed to verify inputs. Skipping")
                
    def _verify_inputs(self, regex, output_dir) :
        """Verify that the rule dected in the file is valid."""

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
        """Execute all the filter rules in the file once."""

        for rule in self.filters :
            bf = BaseFilter(self.target_dir, rule=rule)
            bf.execute()



class BackgroundHandler :
    """
    Object that constantly checks a folder for matches and moves them.

    This class uses a file as an input, but unlike the FileFilter object, a 
    BackgroundHandler will constantly poll a folder to filter it. A single 
    BackgroundHandler takes a single thread to execute. Will change this
    in future updates.

    Attributes:
    target_dir : str
        path to directory that holds the filter file and where filtering will happen
    input_fname : str
        name of the file that holds filter rules. Defaults to 'filters.txt'
    
    Methods:
    execute()
        constantly polls a file for matches every preset amount of time. 
    """

    def __init__ (self, target_dir, input_fname="filters.txt") :
    """
    Parameters:
    target_dir : str
        path to directory in which files will be filtered from
    input_fname : str
        name of file that stores all the filter rules. Located in target_dir.
    """

        self.target_dir = target_dir
        if not os.path.isdir(self.target_dir) :
            raise InputError(self.target_dir, f"{self.output_dir} is not a directory")

        self.input_file = os.path.join(self.target_dir, input_fname)
        if not os.path.isfile(self.input_file) :
            create_filter_file(target_dir=self.target_dir)
            raise InputError(self.target_dir, f"{input_fname} does not exist in {self.target_dir}")

        ff = FileFilter(self.input_file, self.target_dir)
        ff.execute()
        self.filters = ff.filters

    def execute(self) :
    """constantly poll a directory and filter matches"""
        try:
            while True :
                time.sleep(POLL_DELAY)
                #poll directory for matches, and check file for updates
                dir_list = os.listdir(self.target_dir)
                matches = []
                for rule in self.filters :
                    matches = list(filter(rule[0].match, dir_list))

                    #move every detected match
                    for match in matches :
                        os.replace(os.path.join(self.target_dir, match),
                            os.path.join(rule[1], match))

        # this except is only useful when debugging. When running
        # in daemon mode, this exception will never be thrown.
        except KeyboardInterrupt :
            exit(1)



class InputError(Exception) :
    """Exception raised for errors in the script input

    Attributes:
    expression: str
        input expression in which the error occurred
    message : str
        explanation of error
    """

    def __init__(self, expression, message) :
        self.expression = expression
        self.message = message
        super().__init__(message)