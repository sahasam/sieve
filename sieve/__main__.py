"""
sieve

Application that filters files from your downloads. 
Files placed in download folders will automatically filter
and keep your folder neat

Usage:
sieve -r <regex> -o <path>
sieve -i <file> [-ds]

-r <regex>, --regex <regex>         regex expression to match encoding
-o <path>, --output <path>          destination folder for regex exp [default: ./filtered]
-i <file>, --input <file>           file with regex expression and destination folders
-d, --daemon                        run in the background
-s, --startup                       run command on startup (implies daemon)
"""
import logging
from docopt import docopt

from sieve import __version__

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    args = docopt(__doc__, version=f"pyvr version {__version__}", options_first=True)
    logger.debug(args)
    print(args)
    
    if (not args['--regex']==None ) and (not args['--output']==None) :
        print("running quick filter")

    else if args['--startup'] :
        print("installing for startup")

    else if args['--daemon'] :
        print("creating process")







