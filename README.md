# hcp2bids
To convert Human Connectome project data to BIDS Structure.

Clone this github directory:
```
git clone https://github.com/niniko1997/hcp2bids.git
```
Change into the project directory:
```
cd hcp2bids/hcp2bids
```

You can run the code using:
```
usage: main.py [-h] [--symlink] [-d {'T1w', 'freesurfer'}] [-g guid_file]
               input_dir output_dir

positional arguments:
  input_dir             Location of the root of your HCP dataset directory
  output_dir            Directory where BIDS data will be stored

optional arguments:
  -h, --help            show this help message and exit
  --symlink             Creates symlinks for files from input_dir to
                        output_dir and puts the symlinks in BIDS format.
                        Without this flag, the HCP files will be moved from
                        input_dir to output_dir and then put into BIDS format.
  -d {'T1w', 'freesurfer'}
                        Takes HCP files that have undergone extensive
                        preprocessing and puts them into BIDS format. 'T1w'
                        moves processed T1w images into BIDS format.
                        'freesurfer' moves HCP freesurfer output files into
                        BIDS format. If this flag is selected, only the
                        derivatives will be put into BIDS format (not the raw
                        files) in output_dir/derivates.
  -g guid_file          Path to a text file with participant_id to GUID
                        mapping. You will need to use the GUID Tool
                        (https://ndar.nih.gov/contribute.html) to generate
                        GUIDs for your participants.
     
```


Here is an example of running hcp2bids code (in the hcp2bids/hcp2bids directory)
```
python main.py /data/HCP_files /data/HCP_bids --symlink
```

If you just want to put the processed T1w images into BIDS structure, run the following:
```
python main.py /data/HCP_files /data/HCP_bids --symlink -d T1w
```

If you just want to put the HCP freesurfer output into BIDS structure, run the following:
```
python main.py /data/HCP_files /data/HCP_bids --symlink -d freesurfer
```

For both T1w and freesurfer, run
```
python main.py /data/HCP_files /data/HCP_bids --symlink -d T1w -d freesurfer
```