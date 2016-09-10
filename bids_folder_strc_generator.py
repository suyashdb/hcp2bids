# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 09:27:53 2016
Script to move data to respective folder
@author: suyashdb
"""
### getting list of sub_dir path###
import os, glob, shutil
import re

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

d = '/work/04275/suyashdb/lonestar/test_hcp/'

sub_dir = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
for subjects in sub_dir:
    subj_raw =  os.path.join(subjects, 'unprocessed/3T/')
    print(subj_raw)
    #path_bids = '/scratch/04275/suyashdb/hcp/%s/' %subject
    bids = subjects + '/bids/'
    os.mkdir(bids)
    fmap = bids + 'fmap/'
    func = bids + 'func/'
    anat = bids + 'anat/'
    dwi =  bids + 'dwi/'
    os.mkdir(fmap)
    os.mkdir(func)
    os.mkdir(anat)
    os.mkdir(dwi)
    fieldmaplist = glob.glob(os.path.join(subj_raw, '*/*FieldMap*'))
    for fieldmap in fieldmaplist:
        parentdir = os.path.split(os.path.dirname(fieldmap))[1]
        dst = fmap + parentdir +'_'+ os.path.split(fieldmap)[1]
        shutil.move(fieldmap, dst)
    print("done with fMAPs for --", subjects)
    func_list = glob.glob(os.path.join(subj_raw, 't*/*tfMRI*'))
    for func_data in func_list:
        parentdir = os.path.split(os.path.dirname(func_data))[1]
        dst = func + parentdir +'_'+ os.path.split(func_data)[1]
        shutil.move(func_data, dst)
    print("done with func for --", subjects)
    sbref_list = glob.glob(os.path.join(subj_raw, '*/*SBRef*'))
    for sbref in sbref_list:
        parentdir = os.path.split(os.path.dirname(sbref))[1]
        dst = func + parentdir +'_'+ os.path.split(sbref)[1]
        shutil.move(sbref, dst)
    print("done with SBREF's for --", subjects)
    anat_list = glob.glob(os.path.join(subj_raw, 'T*/*3T_T*'))
    for anat_data in anat_list:
        parentdir = os.path.split(os.path.dirname(anat_data))[1]
        dst = anat + parentdir +'_'+ os.path.split(anat_data)[1]
        shutil.move(anat_data, dst)
    print("done with Anat for --", subjects)
    dwi_list = glob.glob(os.path.join(subj_raw, '*/*DWI*'))
    for dwi_data in dwi_list:
        parentdir = os.path.split(os.path.dirname(dwi_data))[1]
        dst = dwi + parentdir +'_'+ os.path.split(dwi_data)[1]
        shutil.move(dwi_data, dst)
    print("done with DWI's for --", subjects)
    dwi_subj_raw = os.path.join(subjects, 'bids/')
    dwi_sbref_list = glob.glob(os.path.join(dwi_subj_raw, '*/*DWI*SBRef*'))
    for sbref in dwi_sbref_list:
        parentdir = os.path.split(os.path.dirname(sbref))[1]
        dst = dwi +'_'+ os.path.split(sbref)[1]
        shutil.move(sbref, dst)
    ''' Sort nifti files and Rename all files as per bids'''
    nifti_func_list = glob.glob(os.path.join(func, '*fMRI*.nii.gz'))
    for nifti_func_file in nifti_func_list:
        filename_split = nifti_func_file.split('_')
        task = filename_split[2]
        print(task)
        acq = filename_split[3]
        sub = filename_split[4].lower()
        if task in ['REST1', 'REST2']:
            #m = re.match(r"([a-zA-Z]+)([0-9]+)",task)
            #run = m.group(2)
            run = '0' + str(task[-1])
            task = str(task[:-1])
            # print("This is task form rest loop - ", task)
        tail = filename_split[-1]
        if task not in ['REST', 'REST2']:
            if 'SBRef' in tail:
                filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_' + tail.lower()
            else:
                filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_bold' + tail[-7:]
        else:
            filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq +'_'+ 'run-' + run + '_' + tail.lower()
        path_filename = func + filename
        shutil.move(nifti_func_file, path_filename)
        touch(path_filename[:-6]+ 'json')
        print(filename)
    ''' sort anat files and rename it '''
    #anat = '/Users/suyashdb/Documents/hcp2bids/hcpdata/285446/bids/anat'
    anat_files_list = glob.glob(os.path.join(anat, '*T*.nii.gz'))
    for anat_file in anat_files_list:
        filename_split = anat_file.split('_')
        run = filename_split[2][-1]
        print(filename_split)
        sub = filename_split[3]
        modality = filename_split[5]
        tail = filename_split[-1][-7:]
        filename = 'sub-' + sub + '_' + 'run-' + run + '_' + modality + tail
        path_filename = anat + filename
        shutil.move(anat_file, path_filename)
        touch(path_filename[:-6]+ 'json')
        print(filename)
        ##########
    #Sort all nii.gz files in dwi and fmaps '''
    dwi_files_list = glob.glob(os.path.join(dwi, 'Diffusion*DWI*.nii.gz'))
    for dwi_file in dwi_files_list:
        filename_split = dwi_file.split('_')
        print(filename_split)
        sub = filename_split[2]
        acq = filename_split[5].lower() + filename_split[6][:2]
        modality = 'dwi'
        tail = filename_split[-1][-7:]
        filename = 'sub-' + sub + '_' + 'acq-' + acq + '_' + modality + tail
        path_filename = dwi + filename
        shutil.move(dwi_file, path_filename)
        touch(path_filename[:-6]+ 'json')
        shutil.move((dwi_file[:-6]+'bval'), (path_filename[:-6] + 'bval'))
        shutil.move((dwi_file[:-6]+'bvec'), (path_filename[:-6] + 'bvec'))
        print(filename)
    dwisbref_files_list = glob.glob(os.path.join(dwi, '*DWI*SBRef.nii.gz'))
    for dwi_file in dwisbref_files_list:
        filename_split = dwi_file.split('_')
        print(filename_split)
        sub = filename_split[3]
        acq = filename_split[6].lower() + filename_split[7][:2]
        modality = 'sbref'
        tail = filename_split[-1][-7:]
        filename = 'sub-' + sub + '_' + 'acq-' + acq + '_' + modality + tail
        path_filename = dwi + filename
        shutil.move(dwi_file, path_filename)
        print(filename)
        touch(path_filename[:-6]+ 'json')
    ''' Fmaps'''
    counter = 1
    fmap_files_list = glob.glob(os.path.join(fmap, '*SpinEchoFieldMap*.nii.gz'))
    for fmapfile in fmap_files_list:
        fmap_file = os.path.split(fmapfile)[1]
        filename_split = fmap_file.split('_')
        print(filename_split)
        task = filename_split[1]
        print(task)
        acq = filename_split[2]
        sub = filename_split[3].lower()
        if task in ['REST1', 'REST2']:
            #m = re.match(r"([a-zA-Z]+)([0-9]+)",task)
            #run = m.group(2)
            run = '0' + str(task[-1])
            task = str(task[:-1])
            print("This is task form rest loop - ", task)
        tail = filename_split[-1]
        if task not in ['REST', 'REST2']:
            if 'SBRef' in tail:
                filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_' + tail.lower()
            else:
                filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_bold' + tail[-7:]
        else:
            filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq +'_'+ 'run-' + run + '_' + tail.lower()
        print('intended_for - ',filename)
        filename = '/func/'+ filename
        intended_for ={"IntendedFor", filename}
        dir = counter
        hcpfmapfilename = 'sub-' + sub + '_'+ 'dir-' + str(dir) + '_' + 'epi.nii.gz'
        print('DWI_filename',hcpfmapfilename)
        path_filename = fmap + hcpfmapfilename
        shutil.move(fmapfile, path_filename)
        touch(path_filename[:-6]+ 'json')
        counter = counter + 1
    ''' Writing Json files'''


fmap_files_list = glob.glob(os.path.join(fmap, '*_FieldMap*.nii.gz'))




import json
json-string = json.dumps(intended_for)


### to find all task.json files and make a copy for sbref.json



#''' Sort json files in func'''
#json_func_list = glob.glob(os.path.join(func, '*fMRI*.json'))
#
#for json_func_file in json_func_list:
#    filename_split = json_func_file.split('_')
#    task = filename_split[1]
#    print(task)
#    acq = filename_split[2]
#    sub = filename_split[3].lower()
#    if task in ['REST1', 'REST2']:
#        #m = re.match(r"([a-zA-Z]+)([0-9]+)",task)
#        #run = m.group(2)
#        run = '0' + str(task[-1])
#    tail = filename_split[-1]
#    if task not in ['REST1', 'REST2']:
#        if 'SBRef' in tail:
#            filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_' + tail.lower()
#        else:
#            filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_bold' + tail[-7:]
#    else:
#        filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq +'_'+ 'run-' + run + '_' + tail.lower()
#    print(filename)
#
#
