import subprocess
import sys

CMD = '/usr/bin/iostat -d -x -t -y 5'

def run_process(exe):    
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while(True):
        retcode = p.poll() #returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if(retcode is not None):
            break

def main():
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    for line in run_process(CMD):
        if !re.match('sd', line):
            next
        fields = line.split()
