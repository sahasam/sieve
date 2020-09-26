# sieve

sieve is a python command line tool I created to organize the messy downloads folder on my mac. I created a file filtering system based on some regex expressions. This has the ability to run entirely in the background and start running when your computer turns on.

### Usage:
##### Single Use:
One time filter. Moves files matching the regex pattern to the `<path>` directory. Pretty much the same as `mv` in bash.
```
sieve -r <regex> -o <path> [-d] [-t <target>]
```

##### Polling filter:
```
sieve [-t <target>] [-f <file>] [-ds]
```
A polling filter constantly checks a directory to see if any files matching filter rules exist. Polling filter rules are stored in a file called `filters.txt` in the polled directory.

```
-t <target>, --target <target>      directory to sort files from [default: ./]
-r <regex>, --regex <regex>         regex expression to match encoding
-o <path>, --output <path>          destination folder for regex exp [default: ./filtered]
-f <file>, --filename <file>        name of file with regex expression and destination folders [default: filters.txt]
-d, --daemon                        run in the background
-s, --startup                       run command on startup (implies daemon)
```

### filters.txt:

A `filters.txt` file is placed in every directory that is constantly polled for matches. A filter file contains simple rules that tell the sieve process how to sort matched files.

An entry in filters.txt looks like the following. Currently, sieve does not support regex expression, or directories, with spaces in them.
```
; Comments can be written with a semicolon in the front
; works:
^hello_world\.txt$  /Users/sahasam/Downloads/txtfiles/

; doesn't work:
^hello[ a-zA-Z0-9]*\.txt$   /Users/sahasam/Downloads/hello numbers/
```

a sample `filters.txt` file can be found in `examples/ex_filters.txt`

if you need some reference for regex expressions, visit [here](https://google.com/).

### Installation:
```
pip install git+https://github.com/sahasam/sieve
```
running this command in the terminal will install the `sieve` command through pip.

### Run on startup:
Because you don't want to run a command every time your computer boot's up. 
##### Mac OS:
1. After installing, open the terminal and run the following.

```
$ which sieve
```
2. Replace the first `<++>` in `examples/com.sieve.filter.plist` with the output from the first command.
3. Replace the second `<++>` in `examples/com.sieve.filter.plist` with the path to the directory where polling will happen (target directory)
4. Place the edited `com.sieve.filter.plist` file into the `~/Library/LaunchAgents` directory with the following command
```
$ mv /path/to/com.sieve.filter.plist ~/Library/LaunchAgents/
```
5. Let MacOS know about the file with the following
```
sudo launchctl load -w ~/Library/LaunchAgents/
```
6. Restart your computer to test. 

