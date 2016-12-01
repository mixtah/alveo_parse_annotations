'''
Created on 1 Dec 2016

@author: Michael
'''

import os,sys,json,csv
import hashlib
from scan import scan_files, parse_args, log

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

data = {}
#columns = ['1_2','1_3','1_4','2_7','2_16','2_22','3_8','3_32','4_10','4_32']
columns = ['speaker']

def pre_dir(**kw):
    log("Scanning: "+kw['dirpath'],kw['outfile'])

def on_file(**kw):
    ''' Searches for particular file names and counts to provide data on how things look '''
    global data
    global columns
    try:
        file,ext = kw['file'].split('.')
        comps = file.split('_')
        speaker = comps[0]+'_'+comps[1]
        session = comps[2]+'_'+comps[3]
        item = comps[4][:3] #This may have -ch6-speaker or -n-n-n behind it
    except:
        #Not an interesting file skip
        return
    
    #Initialize anything that needs it
    if not speaker in data:
        data[speaker] = {}
    
    if not session in data[speaker]:
        data[speaker][session]={}
    
    #For duplicate files
    if not item in data[speaker][session]:
        data[speaker][session][item]={}
    
    #Add in the file data
    path = os.path.join(kw['dirpath'],kw['file'])
    hash = md5(path)
    
    
    if not hash in data[speaker][session][item]:
        data[speaker][session][item][hash] = []
    
    data[speaker][session][item][hash].append(path)
    
    if not session in columns:
        columns.append(session)

def on_finish(**kw):
    ''' output all data '''
    global data
    
    log("Finished Scanning Files",kw['outfile'])
    
    #generate output
    with open(kw['output_file']+'.json','w') as file:
        file.write(json.dumps(data))
        
    log("Finished Generating json output",kw['outfile'])
    
    csv_rows = []
    
    for speaker in data:
        tmp = {'speaker':speaker}
        for session in data[speaker]:
            tmp[session] = len(data[speaker][session])
        csv_rows.append(tmp)
    
    with open(kw['output_file']+'.csv','w') as file:
        dict_writer = csv.DictWriter(file,lineterminator='\n',fieldnames=columns)
        dict_writer.writeheader()
        dict_writer.writerows(csv_rows)
    
    log("Finished Generating csv output",kw['outfile'])

if __name__ == '__main__':
    vars = parse_args(extra_usage="""Scans provided directories and refactors them into a new directory structure.""")
    output_file='annotation_data'
    with open(output_file+'.log','w') as file:
        print "Starting Scan"
        scan_files(vars['root'], outfile=file, function=on_file,on_finish=on_finish,pre_dir=pre_dir,output_file=output_file)