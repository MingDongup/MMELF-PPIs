# MMELF: 
Improving Protein-Protein Interaction Prediction Using Ensemble Learning and Residual Network.

## Pre-requisite:
    - Python3
    - SANN (https://github.com/newtonjoo/sann)
	- NCBI nr database (https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/)
	- PSI-BLAST (http://blast.ncbi.nlm.nih.gov)
    - Linux system 
	
## Installation:

*Install and configure the softwares of Python3, SANN, nr, PSI-BLAST. Please make sure that python3 includes the modules of 'os', 'math', 'numpy', 'random', 'subprocess', 'sys', 'torch' and 'shutil'. If any one modules does not exist, please using 'pip3 install XXXX' command install the python revelant module. Here, "XXXX" is one module name.

*Download this repository at https://github.com/MingDongup/MMELF-PPIs Then, uncompress all files and run the following command lines on Linux System.
~~~
 1. unzip MMELF-PPI.zip
 2. cd MMELF-PPI
~~~

*The file of "Config.ini" should be set as follows:
~~~
 Sann_Runner_Path = xx/SANN/sann/bin/sann.sh
 Psi_Blast_Path = xx/ncbi-blast-2.13.0+/bin/
 DB_PATH =xx/nr/
 Result_Path = xx/out/
~~~
Note that "xx" represent the absolute path.

## Run 
~~~
  $ python MMELF.py xxxx
~~~
NOTE THAT, "xxxx" represent the absolute path to the protein sequence. For example, MMELF.py xxxx/example/test.fasta.
After Running MMELF.py, you will get a file (named PredictionResult) which contains the probability of each residue of the protein sequence to be the binding site.

## Update History:

- First release 2022-6-2

## References

Jun Hu, Ming dong, Biao Zhang, Xiao-Gen zhou, Dong-jun Yu and Gui-Jun Zhang. Improving Protein-Protein Interaction Prediction Using Ensemble Learning and Residual Network