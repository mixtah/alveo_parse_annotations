'''
Created on 28 Nov 2016

@author: Michael
'''

import os,sys
from scan import scan_files

CWD = os.path.dirname(os.path.realpath(__file__))
SRC = "C:\\Users\\Michael\\Desktop\\annotations-organised"
SPACE = "  "


extns = {}
total = {}

def pre_dir(**kw):
    global extns
    extns = {}

def post_dir(**kw):
    #Print Directory Info
    global extns
    s = SPACE*(kw['depth']*2)+kw['dirpath'][len(kw['root']):]
    print s
    if not kw['outfile']==None:
        kw['outfile'].write(s+'\n')
    for i in extns:
        s = SPACE*(kw['depth']*2+1)+"%s : %d" % (i,extns[i])
        print s
        if not kw['outfile']==None:
            kw['outfile'].write(s+'\n')
            
def on_file(**kw):
    global extns
    global total
    spl = kw['file'].split('.')
    if len(spl)==1:
        ext = ''
    else:
        ext = spl[-1]
        
    try:
        extns[ext] = extns[ext]+1
    except KeyError:
        extns[ext] = 1
        
    try:
        total[ext] = total[ext]+1
    except KeyError:
        total[ext] = 1
        
def on_finish(**kw):
    s = "\ntotals:"
    print s
    if not kw['outfile']==None:
        kw['outfile'].write(s+'\n')
    for i in total:
        s = "%s : %d" % (i,total[i])
        print s
        if not kw['outfile']==None:
            kw['outfile'].write(s+'\n')

def usage():
    print "Usage: python scan_file_extns.py <Str: Path to Root Directory> <?Int: Max Depth default=MaxInt>"

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
        scan_files(SRC,max_depth=max_depth, outfile=file, function=on_file, 
                   on_finish=on_finish, pre_dir=pre_dir, post_dir=post_dir)