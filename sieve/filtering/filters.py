#filters.py

#simple filter which does nothing more than
#change directory
class BaseFilter :
    def __init__ (self, target_dir, regex, output_dir):
        self.target_dir = target_dir
        self.regex = regex
        self.output_dir = output_dir

    def execute (self) :
        #match all regex in target and move to output folder
        print("executing... ")
        print("moving %s to %s" % (self.target_dir, self.output_dir))
        print("done\n\n")

        #generate shell command??
        print("mv %s/%s %s" % (self.target_dir, self.regex, self.output_dir))
        print(f"mv {self.target_dir}/{self.regex} {self.output_dir}")
    
#deals with large folders to filter (>50 files)
class MultithreadedFilter (BaseFilter) :
    def __init__ (self, regex, output):
        super.__init__(regex, output)

#class to read input file and create necessary
# filters
class FilterConfig :
    def __init__ ():
        print("u should not have gotten here")

def main():
    bf = BaseFilter(target_dir=".", regex="hello.txt", output_dir="./output/")
    bf.execute()
