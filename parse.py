'''
Created on 25 Nov 2016

@author: Michael
'''

import os,sys
import hashlib

CWD = os.path.dirname(os.path.realpath(__file__))
SRC = "C:\\Users\\Michael\\Desktop\\annotations-organised"
SPACE = "  "

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def display_repeat_files(outfile=None,printdirs=True):
    files = {}
    for dirpath, dirnames, filenames in os.walk(SRC):
        for file in filenames:
            hash = md5(os.path.join(dirpath,file))
            try:
                files[hash][0] = files[hash][0]+1
                files[hash][1].append(os.path.join(dirpath[len(SRC):],file))
            except KeyError:
                files[hash] = [1,[os.path.join(dirpath[len(SRC):],file)]]
        print 'scanned:\t',dirpath
    for i in files:
        if files[i][0]>1:
            s = "%s : %d" % (i,files[i][0])
            if printdirs:
                s = s+'\n\t'+'\n\t'.join(files[i][1])
            print s
            if not file==None:
                outfile.write(s+'\n')
    

def print_folder_info(dirpath="",extns = {},src=SRC,file=None):
    depth = len(dirpath[len(src):].split(os.path.sep))-1
    s = SPACE*(depth*2)+dirpath[len(src):]
    print s
    if not file==None:
        file.write(s+'\n')
    for i in extns:
        s = SPACE*(depth*2+1)+"%s : %d" % (i,extns[i])
        print s
        if not file==None:
            file.write(s+'\n')

def display_file_ext_info(outfile=None):
    extns_totals = {}
    for dirpath, dirnames, filenames in os.walk(SRC):
        extns = {}
        for file in filenames:
            spl = file.split('.')
            if len(spl)==1:
                ext = ''
            else:
                ext = spl[-1]
                
            try:
                extns[ext] = extns[ext]+1
            except KeyError:
                extns[ext] = 1
                
            try:
                extns_totals[ext] = extns_totals[ext]+1
            except KeyError:
                extns_totals[ext] = 1
                
        print_folder_info(dirpath, extns,file=outfile)
    s = "\ntotals:"
    print s
    if not file==None:
        outfile.write(s+'\n')
    for i in extns_totals:
        s = "%s : %d" % (i,extns_totals[i])
        print s
        if not file==None:
            outfile.write(s+'\n')
        

if __name__ == '__main__':
    
    funct = 2
    
    if funct==1:
        #Function 1: organise
        #-Get Root Source directory and destination directory
    
        #-Get all speaker directories and copy them to destination
        
        #-Loop over files in dest and create a directory for each extension type that exists.
        
        print "Not yet implemented"
    elif funct==2:
        #Function 2: get folder and file info
        with open(os.path.join(CWD,"output.txt"),'w') as file: 
            display_file_ext_info(outfile=file)
    elif funct==3:
        #Function 3: find all repeat files, display their directories and how unique they are.
        with open(os.path.join(CWD,"output.txt"),'w') as file: 
            display_repeat_files(outfile=file)
    
    