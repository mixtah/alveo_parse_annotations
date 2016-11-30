'''
Created on 28 Nov 2016

@author: Michael
'''
import os

def log(text,file=None):
    print text
    if not file==None:
        file.write(text+'\n')

def delete_file_of_type(**kw):
    if not 'type' in kw:
        return
    spl = kw['file'].split('.')
    if len(spl)==1:
        ext = ''
    else:
        ext = spl[-1]
    if ext==kw['type']:
        path = os.path.join(kw['dirpath'],kw['file'])
        os.remove(path)
        log("Deleted: %s" % (path),kw['outfile'])
        
def convert_file_prefix_if_new(**kw):
    ''' Some files have a silly prefix and are supposedly newer, 
        convert these just like 'convert_file_type_if_new' '''
    if not 'prefix' in kw:
        return
    
    if kw['file'][:len(kw['prefix'])]==kw['prefix']:
        to_file_name = kw['file'][len(kw['prefix']):]
        to_file_full_dir = os.path.join(kw['dirpath'],to_file_name)
        from_file_full_dir = os.path.join(kw['dirpath'],kw['file'])
        from_file_time = os.path.getmtime(from_file_full_dir)
        try:
            to_file_time = os.path.getmtime(to_file_full_dir)
        except:
            #to_file doesn't exist so rename to to_filename
            os.rename(from_file_full_dir, to_file_full_dir)
            log("Converted: %s" % (from_file_full_dir),kw['outfile'])
        else:
            #to_file exists, 
            #TODO: check the direction of this time check, something seemed off when less than
            if from_file_time>to_file_time:
                #exists but is older,delete from_file
                os.remove(from_file_full_dir)
                log("Deleted: %s" % (from_file_full_dir),kw['outfile'])
            else:
                #exists and is newer, delete it and rename
                os.remove(to_file_full_dir)
                log("Deleted: %s" % (to_file_full_dir),kw['outfile'])
                os.rename(from_file_full_dir, to_file_full_dir)
                log("Converted: %s" % (from_file_full_dir),kw['outfile'])
            
def convert_file_type_if_new(**kw):
    ''' Given any file of a particular extension, it will be renamed to the desired 
        extension and override only if the file is newer that any file currently named
        as such. If older than the file will be deleted.
        Will result in no files with the old extension.'''
    if not 'from_type' in kw:
        return
    if not 'to_type' in kw:
        return
    spl = kw['file'].split('.')
    if len(spl)==1:
        ext = ''
    else:
        ext = spl[-1]
    if ext==kw['from_type']:
        to_file_name = kw['file'][:-len(kw['from_type'])]+kw['to_type']
        to_file_full_dir = os.path.join(kw['dirpath'],to_file_name)
        from_file_full_dir = os.path.join(kw['dirpath'],kw['file'])
        from_file_time = os.path.getmtime(from_file_full_dir)
        try:
            to_file_time = os.path.getmtime(to_file_full_dir)
        except:
            #to_file doesn't exist so rename to to_filename
            os.rename(from_file_full_dir, to_file_full_dir)
            log("Converted: %s" % (from_file_full_dir),kw['outfile'])
        else:
            #to_file exists, 
            #TODO: check the direction of this time check, something seemed off when less than
            if from_file_time>to_file_time:
                #exists but is older,delete from_file
                os.remove(from_file_full_dir)
                log("Deleted: %s" % (from_file_full_dir),kw['outfile'])
            else:
                #exists and is newer, delete it and rename
                os.remove(to_file_full_dir)
                log("Deleted: %s" % (to_file_full_dir),kw['outfile'])
                os.rename(from_file_full_dir, to_file_full_dir)
                log("Converted: %s" % (from_file_full_dir),kw['outfile'])
            
