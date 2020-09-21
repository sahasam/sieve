#!/usr/bin/python3
"""
sieve

Application that filters files from your downloads. 
Files placed in download folders will automatically filter
and keep your folder neat

Usage:
sieve -r <regex> -o <path> [-d] [-t <target>]
sieve [-t <target>] [-f <file>] [-ds]

-t <target>, --target <target>      directory to sort files from [default: ./]
-r <regex>, --regex <regex>         regex expression to match encoding
-o <path>, --output <path>          destination folder for regex exp [default: ./filtered]
-f <file>, --filename <file>        name of file with regex expression and destination folders [default: filters.txt]
-d, --daemon                        run in the background
-s, --startup                       run command on startup (implies daemon)
-h, --help
"""
import time
from docopt import docopt

from sieve import __version__

def main():
    args = docopt(__doc__, version=f"sieve version {__version__}", options_first=True)
    logger.debug(args)
    
    if (not args['--regex']==None ) and (not args['--output']==None) :
        from sieve.filtering.filters import baseFilter

        bf = BaseFilter(target_dir=args['--target'],
            regex=args['--regex'],
            output_dir=args['--output'])
        bf.execute()
    elif args['--startup'] :
        print("installing for startup")

    elif args['--daemon'] :
        from sieve.filtering.filters import BackgroundHandler

        bh = BackgroundHandler(target_dir=args['--target'],
            input_fname=args['--filename'])
        bh.execute()
    else :
        from sieve.filtering.filters import FileFilter

        ff = FileFilter(input_file=args['--filename'],
            target_dir=args['--target'])
        ff.execute()