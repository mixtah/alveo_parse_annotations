'''
Created on 28 Nov 2016

@author: Michael
'''

import os,sys,time

CWD = os.path.dirname(os.path.realpath(__file__))

defaults = {'max_depth':sys.maxint,
            'output':os.path.join(CWD,"output.txt"),
            'module':None,
            'function':None,
            'pre_dir':None,
            'post_dir':None,
            'on_start':None,
            'on_finish':None,
            'detail':'info',
            'stop_on_error':'true',
            'append_output':'false'
            }

def log(text,file=None):
    print text
    if not file==None:
        file.write(text+'\n')

def print_files(**kw):
    log(os.path.join(kw['dirpath'],kw['file']),kw['outfile'])
    
def print_dirs(**kw):
    log(kw['dirpath'],kw['outfile'])

def print_kwargs(**kw):
    s = 'kwArgs:\n'+'\n'.join(str(key)+':'+str(value) for key,value in kw.items())
    log(s,kw['outfile'])


def scan_files(src,function=None,pre_dir=None,post_dir=None,outfile=None,
               on_start=None,on_finish=None,**kwargs):
    try:
        detail = kwargs['detail']
    except:
        detail = 'none'
    try:
        max_depth = int(kwargs['max_depth'])
    except:
        max_depth = sys.maxint
    #This may seem like a bit of redundancy but it forces root to be a variable
    if not src in kwargs:
        kwargs['root'] = src
    #Call On_Start
    if not on_start==None:
        on_start(outfile=outfile,**kwargs)
    for dirpath, dirnames, filenames in os.walk(src):
        depth = len(dirpath[len(src):].split(os.path.sep))-1
        if depth<=max_depth:
            if not pre_dir==None:
                pre_dir(depth=depth,outfile=outfile,dirpath=dirpath,dirnames=dirnames,filenames=filenames,**kwargs)
            #Call dir_function
            for file in filenames:
                #Call function
                if not function==None:
                    function(depth=depth,outfile=outfile,file=file,dirpath=dirpath,**kwargs)
            if detail in ['verbose','debug']:
                log('scanned:\t'+dirpath,outfile)
            if not post_dir==None:
                post_dir(depth=depth,outfile=outfile,dirpath=dirpath,dirnames=dirnames,filenames=filenames,**kwargs)
            
    #Call On_Finish
    if not on_finish==None:
        on_finish(outfile=outfile,**kwargs)
    
def usage(extra=''):
    print "Usage: python file_extn.py <Key>=<Value> <Key>=<Value> ..."
    print ""
    print extra
    print ""
    print "Standard Keys:"
    print "root\t\t Root Directory, Must be provided"
    print "max_depth\t Max Depth into folder structure the script will run. Default: Integer Max"
    print "output\t\t A file path for the output to be printed to. Default: output.txt in the same folder as the script"
    print "module\t\t A module to be loaded for custom functions. Default: None"
    print "function\t Function to be run on each file. Default: None" 
    print "pre_dir\t\t Function to run once before accessing each directory Default: None"
    print "post_dir\t Function to run once after accessing each directory Default: None"
    print "on_start\t Function run before beginning the scan. Default: None"
    print "on_finish\t Function run after beginning the scan. Default: None"
    print "detail\t\t Describes how detailed the output is. Default: info" 
    print "stop_on_error\t Boolean, continues scan and skips section on error if false, Default: true" 
    print "append_output\t Boolean, will append to output file rather than overriding if true, Default: true" 
    print ""
    print "All Keywords including custom keys will be passed to each function"
    exit()

def parse_args(default=defaults,extra_usage='',required=['root']):
    """ Gets sys.argv and expecting a <Key>=<Value> format. Prints usage on error or request.
        @var extra_usage: Text that is added at the end of the help text so custom entries can be added. 
        @Return dict with all given key/value combinations """
    
    vars = default
    
    if len(sys.argv)<2:
        usage("Error: You must at least pass the following arguments!\n%s\n%s"%(str(required),extra_usage))
    
    #Some things someone may type to get help
    if sys.argv[1] in ['-h','--help','help','usage']:
        usage(extra_usage)
    
    for i in range(1,len(sys.argv)):
        s = sys.argv[i].split('=')
        if not len(s)==2:
            usage("""Error: Incorrectly formatted Arguments, please use <Key>=<Value> !\n
            Avoid any space characters and the equals sign.\n%s\n"""%extra_usage)
        vars[s[0]] = s[1]
    
    for req in required:
        if not req in vars:
            usage("Error: You must include the '%s' field!\n%s\n"%(req,extra_usage))
        
    return vars

if __name__ == '__main__':
    
    #TODO: stop_on_error handling
    #TODO: handle spaces in some names (they'll need quotation marks)
    
    vars = parse_args()
    
    function = None
    pre_dir = None
    post_dir = None
    on_start = None
    on_finish = None
    
    if vars['module']==None:
        #No module defined so the function must be defined here
        #If not let python throw error
        try:
            if not vars['function']==None:
                function = globals()[vars['function']]
            if not vars['pre_dir']==None:
                pre_dir = globals()[vars['pre_dir']]
            if not vars['post_dir']==None:
                post_dir = globals()[vars['post_dir']]
            if not vars['on_start']==None:
                on_start = globals()[vars['on_start']]
            if not vars['on_finish']==None:
                on_finish = globals()[vars['on_finish']]
        except KeyError:
            print "A function name was provided that doesn't exist!"
            raise
    else:
        #Custom module given, so we'll load the functions from there
        #Let python complain if the module or functions don't exist.
        module = __import__(vars['module'])
        if not vars['function']==None:
            function = getattr(module,vars['function'])
        if not vars['pre_dir']==None:
            pre_dir = getattr(module,vars['pre_dir'])
        if not vars['post_dir']==None:
            post_dir = getattr(module,vars['post_dir'])
        if not vars['on_start']==None:
            on_start = getattr(module,vars['on_start'])
        if not vars['on_finish']==None:
            on_finish = getattr(module,vars['on_finish'])
    
    with open(vars['output'],'w') as file: 
        start = time.time()
        if vars['detail'] in ['verbose','debug','info']:
            log('Starting Scan: Start Time = %s\nArgs:' % time.strftime('%Y-%m-%d %H:%M:%S'),file)
            log('\n'.join(str(key)+':'+str(value) for key,value in vars.items()),file)
        
        #To avoid repeats as the functions themselves are passed directly and may be on the same name.
        del vars['module']
        del vars['function']
        del vars['pre_dir']
        del vars['post_dir']
        del vars['on_start']
        del vars['on_finish']
        del vars['output']
        
        #Run base function
        scan_files(vars['root'],
                   outfile=file,
                   function=function,
                   pre_dir=pre_dir,
                   post_dir=post_dir,
                   on_start=on_start,
                   on_finish=on_finish,
                   **vars)
        
        finish = time.time()
        if vars['detail'] in ['verbose','debug','info']:
            log('Finished Scan: End Time = %s\nDuration (seconds) %d' 
                % (time.strftime('%Y-%m-%d %H:%M:%S'),finish-start),file)
            