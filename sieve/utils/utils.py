#utils.py
import os
from pkg_resources import resource_stream
from shutil import copyfileobj

def create_filter_file(target_dir="./") :
    with open(os.path.join(target_dir, "filters.txt"), 'wb+') as filter_file :
        _template = resource_stream('sieve.resources', 'filters.txt')
        copyfileobj(_template, filter_file)






