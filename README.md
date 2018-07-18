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
usage: main.py [-h] [-s --symlink] [-g --guid_mapping] input_dir output_dir

    positional arguments:
    input_dir          Location of the root of your HCP dataset directory
    output_dir         Directory where BIDS data will be stored

   optional arguments:
   -h, --help         show this help message and exit
   -s --symlink       Type t for true and f for false. If true, symlinks will be created for files from input_dir to
                      output_dir and put the symlinks in BIDS format. If false, files from input_dir will be moved
                      to output_dir and then put into BIDS format.
   -g --guid_mapping  Path to a text file with participant_id to GUID mapping.
                      You will need to use the GUID Tool
                      (https://ndar.nih.gov/contribute.html) to generate GUIDs
                      for your participants.
     
```

Here is an example of running the code (in the hcp2bids/hcp2bids director)
```
python main.py /data/HCP_files /data/HCP_bids_files -s t
```
