'''
Created on 28 Nov 2016

@author: Michael
'''
import os

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
        s = "Deleted: %s" % (path)
        print s
        if not kw['outfile']==None:
            kw['outfile'].write(s+'\n')
            
