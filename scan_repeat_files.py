'''
Created on 28 Nov 2016

@author: Michael
'''

import os,sys
import hashlib
from scan import scan_files

CWD = os.path.dirname(os.path.realpath(__file__))
SRC = ""

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

files = {}

def on_file(**kw):
    global files
    hash = md5(os.path.join(kw['dirpath'],kw['file']))
    try:
        files[hash][0] = files[hash][0]+1
        files[hash][1].append(os.path.join(kw['dirpath'][len(kw['root']):],kw['file']))
    except KeyError:
        files[hash] = [1,[os.path.join(kw['dirpath'][len(kw['root']):],kw['file'])]]

def on_finish(**kw):
    try:
        printdirs = kw['printdirs'].lower()=='true'
    except KeyError:
        printdirs = True
    for i in files:
        if files[i][0]>1:
            s = "%s : %d" % (i,files[i][0])
            if printdirs:
                s = s+'\n\t'+'\n\t'.join(files[i][1])
            print s
            if not kw['outfile']==None:
                kw['outfile'].write(s+'\n')

def usage():
    print "Usage: python scan_repeat_files.py <Str: Path to Root Directory> <?Int: Max Depth default=MaxInt>"

if __name__ == '__main__':
    
    max_depth = sys.maxint
    
    if len(sys.argv)>3 or len(sys.argv)<2:
        usage()
    if len(sys.argv)==3:
        try:
            max_depth = int(sys.argv[2])
        except:
            usage()
    SRC = sys.argv[1]
    
    with open(os.path.join(CWD,"output.txt"),'w') as file: 
        scan_files(SRC,max_depth=max_depth, outfile=file, function=on_file, on_finish=on_finish)