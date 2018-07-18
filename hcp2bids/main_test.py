# -*- coding: utf-8 -*-
"""
Created on Aug 2016
Script to save HCP data into bids format. folowing script creates directory struc
ture and renames all files as per BIDS standard.
@author: Suyash B
"""

import os, glob, shutil
import re, json, numpy
import nibabel as ni



def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def FourDimImg(image, destinationpath_3d, outputfilename):
    #outputfilename= sub-285345_run-02_magnitude2
    #this function handles conversion from 4d to 3d along with saving output with bids std name
    img = ni.load(image)
    destination_path = destinationpath_3d
    images = ni.four_to_three(img)
    outputfilenamepattern = outputfilename + '{:01d}.nii.gz'
    for i, img_3d in enumerate(images):
        i = i +1
        output_filename = outputfilenamepattern.format(i)
        output_path = os.path.join(destination_path, output_filename)
        ni.save(img_3d, output_path)
    os.remove(image)
    return img_3d


def hcp2bids(input_dir, output_dir, s_link = False):
    import os 

    #get hcp subject directory paths
    sub_dir = [os.path.join(input_dir,o) for o in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir,o))]
    

    for subjects in sub_dir:
        subj_raw =  os.path.join(subjects, 'unprocessed/3T/')
        print(subj_raw)
        #path_bids = '/scratch/04275/suyashdb/hcp/%s/' %subject

        #output directory for the subject
        bids = os.path.join(output_dir, subjects.split('/')[-1])
        #bids = subjects + '/bids/'
        if not os.path.exists(bids):
            os.mkdir(bids)

        #output directory paths for fmap, func, anat and dwi
        fmap = os.path.join(bids, 'fmap/')
        func = os.path.join(bids, 'func/')
        anat = os.path.join(bids, 'anat/')
        dwi =  os.path.join(bids,'dwi/')
        
        if not os.path.exists(fmap):
            os.mkdir(fmap)
        
        if not os.path.exists(func):
            os.mkdir(func)

        if not os.path.exists(anat):
            os.mkdir(anat)

        if not os.path.exists(dwi):
            os.mkdir(dwi)

        '''Get raw Nifti files from the HCP input directory and move 
        it to the output directory'''
        fieldmaplist = glob.glob(os.path.join(subj_raw, '*/*FieldMap*'))
        for fieldmap in fieldmaplist:
            parentdir = os.path.split(os.path.dirname(fieldmap))[1]
            dst = fmap + parentdir +'_'+ os.path.split(fieldmap)[1]
            shutil.copy(fieldmap, dst)
        print("done with fMAPs for --", subjects)

        func_list = glob.glob(os.path.join(subj_raw, 't*/*tfMRI*'))
        for func_data in func_list:
            parentdir = os.path.split(os.path.dirname(func_data))[1]
            dst = func + parentdir +'_'+ os.path.split(func_data)[1]

            if s_link:
                if not os.path.islink(dst):
                    os.symlink(func_data, dst)
            else:
                shutil.move(func_data, dst)
        print("done with func for --", subjects)

        sbref_list = glob.glob(os.path.join(subj_raw, '*/*SBRef*'))
        for sbref in sbref_list:
            parentdir = os.path.split(os.path.dirname(sbref))[1]
            dst = func + parentdir +'_'+ os.path.split(sbref)[1]
            
            if s_link:
                if not os.path.islink(dst):
                    os.symlink(sbref, dst)
            else:
                shutil.move(sbref, dst)
        print("done with SBREF's for --", subjects)

        anat_list = glob.glob(os.path.join(subj_raw, 'T*/*3T_T*'))
        for anat_data in anat_list:
            parentdir = os.path.split(os.path.dirname(anat_data))[1]
            dst = anat + parentdir +'_'+ os.path.split(anat_data)[1]
            if s_link:
                if not os.path.islink(dst):
                    os.symlink(anat_data, dst)
            else:
                shutil.move(anat_data, dst)
        print("done with Anat for --", subjects)

        dwi_list = glob.glob(os.path.join(subj_raw, '*/*DWI*'))
        for dwi_data in dwi_list:
            parentdir = os.path.split(os.path.dirname(dwi_data))[1]
            dst = dwi + parentdir +'_'+ os.path.split(dwi_data)[1]
            if s_link:
                if not os.path.islink(dst):
                    os.symlink(dwi_data, dst)
            else:
                shutil.move(dwi_data, dst) 
        print("done with DWI's for --", subjects)

        dwi_subj_raw = os.path.join(subjects, 'bids')
        dwi_sbref_list = glob.glob(os.path.join(func,'*DWI*SBRef*'))
        for sbref in dwi_sbref_list:
            parentdir = os.path.split(os.path.dirname(sbref))[1]
            dst = dwi +'_'+ os.path.split(sbref)[1]
            shutil.move(sbref, dst)

        ''' Sort nifti files and Rename all files as per bids'''

        '''Sort func files and rename all per bids'''
        nifti_func_list = glob.glob(os.path.join(func, '*fMRI*.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(func, '*fMRI*.nii.gz'))
        print(len(nifti_func_list))
        for nifti_func_file in nifti_func_list:
            filename_split = nifti_func_file.split('/')
            task = filename_split[3].split('_')[1]
            #acq = filename_split[3]
            #print("Acq", acq)
            sub = filename_split[1].lower()

            if task in ['REST1', 'REST2']:
                #m = re.match(r"([a-zA-Z]+)([0-9]+)",task)
                #run = m.group(2)
                run = '0' + str(task[-1])
                task = str(task[:-1])
                # print("This is task form rest loop - ", task)
            
            tail = filename_split[-1].split('_')[-1]

            if task not in ['REST', 'REST2']:
                if 'SBRef' in tail:
                    #filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_' + tail.lower()
                    filename = 'sub-' + sub + '_' + 'task-' + task + '_' + tail.lower()
                else:
                    #filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq + '_bold' + tail[-7:]
                    filename = 'sub-' + sub + '_' + 'task-' + task + '_bold' + tail[-7:]
            else:
                #filename = 'sub-' + sub + '_' + 'task-' + task + '_' +  'acq-' + acq +'_'+ 'run-' + run + '_' + tail.lower()
                filename = 'sub-' + sub + '_' + 'task-' + task + '_' +'run-' + run + '_' + tail.lower()
            
            path_filename = func + filename
            print(path_filename)

            if not os.path.isfile(path_filename):
                basedir = os.path.dirname(path_filename)
                if not os.path.exists(basedir):
                    os.makedirs(basedir)

            shutil.move(nifti_func_file, path_filename)

            #touch(path_filename[:-6]+ 'json')

        ''' sort anat files and rename it '''
        #anat = '/Users/suyashdb/Documents/hcp2bids/hcpdata/285446/bids/anat'
        anat_files_list = glob.glob(os.path.join(anat, '*T*.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(anat, '*T*.nii.gz'))
        print(len(anat_files_list))
        for anat_file in anat_files_list:
            filename_split = anat_file.split('/')
            sub = filename_split[1]
            modality = filename_split[3].split('_')[0]
            tail = filename_split[3][-7:]

            run = str(1)
            filename = 'sub-' + sub + '_' + 'run-0' + run + '_' + modality + tail
            path_filename = anat + filename

            while os.path.isfile(path_filename):
                run = str(int(run) + 1)
                filename = 'sub-' + sub + '_' + 'run-0' + run + '_' + modality + tail
                path_filename = anat + filename
            
            print(path_filename)
            shutil.move(anat_file, path_filename)
            #touch(path_filename[:-6]+ 'json')
        
            #########
        #Sort all nii.gz files in dwi and fmaps '''
        dwi_files_list = glob.glob(os.path.join(dwi, 'Diffusion*DWI*.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(dwi, 'Diffusion*DWI*.nii.gz'))
        for dwi_file in dwi_files_list:
            filename_split = dwi_file.split('/')
          
            sub = filename_split[1]
            acq = filename_split[-1].split('_')[4].lower() + filename_split[-1].split('_')[5][:2].lower()

            if "SBRef.nii.gz" in filename_split[-1].split('_'):
                # filename = 'sub-' + sub + '_' + 'task-' + 'DWI' + '_' + 'sbref' + tail
                # path_filename = func + filename
                # shutil.move(dwi_file, path_filename)
                # print(path_filename)
                continue

            modality = 'dwi'
            tail = filename_split[-1][-7:]
        
            filename = 'sub-' + sub + '_' + 'acq-' + acq + '_' + modality + tail
            path_filename = dwi + filename
        
            print(path_filename)    
            if not os.path.isfile(path_filename):
                basedir = os.path.dirname(path_filename)
                if not os.path.exists(basedir):
                    os.makedirs(basedir)
            
            shutil.move(dwi_file, path_filename)
            
            dwi_json_dict = {}
            dwi_json_dict["EffectiveEchoSpacing"] = 0.00078
            dwi_json_dict["TotalReadoutTime"] = 0.60
            dwi_json_dict["EchoTime"] = 0.08950
        
            if dwi_file[-9:-7] == 'LR':
                dwi_json_dict["PhaseEncodingDirection"] = "i-"
            else:
                dwi_json_dict["PhaseEncodingDirection"] = "i"
        
            touch(path_filename[:-6]+ 'json')
            json_file = path_filename[:-6]+ 'json'
            with open(json_file, 'w') as editfile:
                json.dump( dwi_json_dict, editfile, indent = 4)
            
            shutil.move((dwi_file[:-6]+'bval'), (path_filename[:-6] + 'bval'))
            shutil.move((dwi_file[:-6]+'bvec'), (path_filename[:-6] + 'bvec'))
        
        dwisbref_files_list = glob.glob(os.path.join(dwi, '*DWI*SBRef.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(dwi, '*DWI*SBRef.nii.gz'))
        for dwi_file in dwisbref_files_list:
            filename_split = dwi_file.split('/')
            sub = filename_split[1]
            acq = filename_split[-1].split('_')[-3].lower() + filename_split[-1].split('_')[-2].lower()
            modality = 'sbref'
            tail = filename_split[-1][-7:]
            filename = 'sub-' + sub + '_' + 'acq-' + acq + '_' + modality + tail
            
            path_filename = dwi + filename
            
            shutil.move(dwi_file, path_filename)
            
            print(path_filename)
            dwi_json_dict = {}
            dwi_json_dict["EffectiveEchoSpacing"] = 0.00078
            dwi_json_dict["TotalReadoutTime"] = 0.60
            dwi_json_dict["EchoTime"] = 0.08950
            
            if filename_split[-1].split('_')[-2][:2] == 'LR':
                dwi_json_dict["PhaseEncodingDirection"] = "i-"
            else:
                dwi_json_dict["PhaseEncodingDirection"] = "i"
            
            touch(path_filename[:-6]+ 'json')
            json_file = path_filename[:-6]+ 'json'
            with open(json_file, 'w') as editfile:
                json.dump( dwi_json_dict, editfile, indent = 4)
        
        ''' Fmaps'''
        counter = 1
        fmap_files_list = glob.glob(os.path.join(fmap, '*SpinEchoFieldMap*.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(fmap, '*SpinEchoFieldMap*.nii.gz'))
        print(len(fmap_files_list))
        for fmapfile in fmap_files_list:
            fmap_file = os.path.split(fmapfile)[1]
            filename_split = fmap_file.split('_')

            task = filename_split[1]
            acq = filename_split[2]
            sub = filename_split[3].lower()
            #print("Task:", task, "\tAcq:", acq, "\tSub:", sub)
        
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
        
            filename = 'func/'+ filename
            fmap_json_dict = {}
            fmap_json_dict["intended_for"] = filename
        
            fmap_json_dict["TotalReadoutTime"] = 0.08346
        
            if fmapfile[-9:-7] == 'LR':
                fmap_json_dict["PhaseEncodingDirection"] = "i-"
            else:
                fmap_json_dict["PhaseEncodingDirection"] = "i"
            #intended_for ={"IntendedFor", filename}
            dir = counter
        
            hcpfmapfilename = 'sub-' + sub + '_'+ 'dir-' + str(dir) + '_' + 'epi.nii.gz'
            print('hcpfmap_filename',hcpfmapfilename)
         
            path_filename = fmap + hcpfmapfilename
            
            shutil.move(fmapfile, path_filename)
        
            touch(path_filename[:-6]+ 'json')
            json_file = path_filename[:-6]+ 'json'
            with open(json_file, 'w') as editfile:
                json.dump( fmap_json_dict, editfile, indent = 4)
            counter = counter + 1

        #fmap_magnitude and phasediff
        
        fmap_files_list = glob.glob(os.path.join(fmap, 'T*Magnitude.nii.gz'))
        print("\npath where nifti files are searched -", os.path.join(fmap, 'T*Magnitude.nii.gz'))
        run = 1
        for fmapfile in fmap_files_list:
            fmap_file = os.path.split(fmapfile)[1]
            filename_split = fmap_file.split('_')
            acq = filename_split[1]
            sub = filename_split[2]
            run_number = filename_split[1][-1]
            filename = 'sub-' + sub + '_' + 'run-0' + str(run) + '_magnitude'
          
            print(filename)   
            #looking into phasediff image
            filename_phasediff = 'sub-' + sub + '_' + 'run-0' + str(run) + '_phasediff' + '.nii.gz'
            filename_phasediff_path = os.path.join(fmap,filename_phasediff)
            
            shutil.move(fmapfile.replace('Magnitude', 'Phase'), filename_phasediff_path)
            
            filename_phasediff_json = filename_phasediff[:-6]+ 'json'
            filename_phasediff_json_path = os.path.join(fmap, filename_phasediff_json)
            touch(filename_phasediff_json_path)
        
            intended_for_filename = 'anat/sub-' + sub + '_' + 'run-0' + run_number + '_' + filename_split[0] + '.nii.gz'
            print('intended_for - ',intended_for_filename)
            
            fmap_phasdiff_json_dict = {}
            fmap_phasdiff_json_dict["intended_for"] = intended_for_filename
            if filename_split[0] == 'T1w':
                fmap_phasdiff_json_dict["EchoTime1"] = 0.00214
                fmap_phasdiff_json_dict["EchoTime2"] = 0.00460
            if filename_split[0] == 'T2w':
                fmap_phasdiff_json_dict["EchoTime1"] = 0.00565
                fmap_phasdiff_json_dict["EchoTime2"] = 0.00811
            with open(filename_phasediff_json_path, 'w') as editfile:
                json.dump( fmap_phasdiff_json_dict, editfile, indent = 4)
            run = run + 1

        print("\n\nBIDS format data is at -", output_dir)

## main.py
##get input and output dir from user
# hcp2bids('/work/04275/suyashdb/lonestar/test_hcp1/', '/work/04275/suyashdb/lonestar/test_output/')
# output_dir = '/work/04275/suyashdb/lonestar/test_output/'


def arrange_subjects(output_dir):
    # find all the subjects in the output dir
    sub_dir = [os.path.join(output_dir,o) for o in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir,o))]
    for subjects in sub_dir:
        # rename all subjects sub-{subject_number}
        sub = subjects.split('/')[-1]
        dir_name = 'sub-'+ sub
        dir_name_path = os.path.join(output_dir, dir_name)
        shutil.move(subjects, dir_name_path)

#task json files
def json_toplevel(output_dir):
    tasks = ['EMOTION', 'GAMBLING', 'LANGUAGE', 'RELATIONAL', 'MOTOR', 'SOCIAL', 'WM', 'REST']
    for task in tasks:
        filename = os.path.join(output_dir, 'task-%s_acq-RL_bold.json' %task)
        touch(filename)
        filename = os.path.join(output_dir, 'task-%s_acq-LR_bold.json' %task)
        touch(filename)
        filename = os.path.join(output_dir, 'task-%s_acq-RL_sbref.json' %task)
        touch(filename)
        filename = os.path.join(output_dir, 'task-%s_acq-LR_sbref.json' %task)
        touch(filename)
    json_task_files = glob.glob(os.path.join(output_dir, 'task*.json'))
    #declare dict with common scan_parameters
    bold_json_dict = {
    "RepetitionTime": 0.72,
    "EchoTime": 0.058,
    "EffectiveEchoSpacing": 0.00058,
    "MagneticFieldStrength": 3.0,
    "TaskName": "Gambling",
    "Manufacturer": "Siemens",
    "ManufacturerModelName": "Skyra"
    }
    for json_file in json_task_files:
        LR = re.search('acq-LR', json_file)
        if LR is not None:
            print("its LR ")
            addline = {"PhaseEncodingDirection": "i"}
        RL = re.search('acq-RL', json_file)
        if RL is not None:
            print("its RL ")
            addline = {"PhaseEncodingDirection": "i-"}
        # addline = { "EffectiveEchoSpacing" : 0.0058}
        z = bold_json_dict.copy()
        z.update(addline)
        print("updated", json_file)
        with open(json_file, 'w') as editfile:
            json.dump( z, editfile, indent = 4)

def main():
    import argparse
    import sys

    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(
        description="BIDS to NDA converter. This software sucks because Chris wrote it. But it's better because Nino's fixing it.",
        fromfile_prefix_chars='@',
        )
    # TODO Specify your real parameters here.
    parser.add_argument(
        "input_dir",
        help="Location of the root of your HCP dataset directory",
        metavar="input_dir")
    parser.add_argument(
        "guid_mapping",
        help="Path to a text file with participant_id to GUID mapping. You will need to use the "
             "GUID Tool (https://ndar.nih.gov/contribute.html) to generate GUIDs for your participants.",
        metavar="GUID_MAPPING")
    parser.add_argument(
        "output_dir",
        help="Directory where BIDS data will be stored",
        metavar="output_dir")
    parser.add_argument(
        "-s",
        help="Type t for true and f for false. Whether the HCP2BIDS should symlink files or move them to output_dir",
        metavar = "--symlink",
        default = 'f'
    )
    args = parser.parse_args()

    input_dir = vars(args)['input_dir']
    guid_map = vars(args)['guid_mapping']
    output_dir = vars(args)['output_dir']

    if vars(args)['s'] == 't':
        symlink = True
    else:
        symlink = False

    print("Input Directory: ", input_dir)
    print("GUID Mapping", guid_map)
    print("Output Directory: ", output_dir)
    print("Symlink: ", symlink)

    print("\nMetadata extraction complete.")

    print("\nRunning hcp2bids")
    hcp2bids(input_dir, output_dir, s_link = symlink)

    print("\nRunning arrange_subjects")
    arrange_subjects(output_dir)

    print("\nRunning json_toplevel")
    json_toplevel(output_dir)

if __name__ == '__main__':
    main()
