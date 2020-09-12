import sys
import os

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null') :
    #first fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(1)         #exit original process, making new fork an orphan controlled by init
    except OSError as e :
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)

    #decouple from parent environment
    os.chdir('/')               #change to a directory that is guaranteed to exist no matter what
    os.umask(0)                 #give highest file permissions
    os.setsid()

    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0)         #exit second parent
    except OSError as e :
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    
    #process is now daemonized, redirect standard file descriptors
    for f in sys.stdout, sys.stderr : 
        f.flush()         #flush buffers
    
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+')
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))