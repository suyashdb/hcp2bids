# hcp2bids
To convert Human Connectome project data to BIDS std.

usage: hcp2bids [-h] [-v] Input_directory output_dir

    positional arguments:
      Input_directory    Location of the root of your HCP dataset

      output_dir  Directory where bids dataset will be stored

    optional arguments:
      -h, --help        show this help message and exit
Example:  hcp2bids /work/04275/suyashdb/lonestar/test_hcp /work/04275/suyashdb/lonestar/test_output
