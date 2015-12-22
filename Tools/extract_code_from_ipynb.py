"""
Usage: python extract_code_from_ipynb.py notebook.ipynb newfile.py
Returns "clean" Python script (*.py) without notebook formatting and without cell output

Full path of input and/or output file can be used.
"""

import sys
import io
import os
from IPython.nbformat import read, write


# SET INPUT FILE NAME:

# Error message:
if len(sys.argv)<2:
    "No input file given. "
    print "input="
    inputfile = raw_input("Please, enter file name (full path if not in current directory): ")
else:
    inputfile = sys.argv[1]
    
#SET OUTPUT FILE NAME

# If no output file name is given, set one using name of input file
if len(sys.argv)<3:
    filename = os.path.splitext(os.path.basename(inputfile))[0]
    outputfile = "%s_extracted.py" % (filename)
else:
    outputfile = sys.argv[2]

# READ INPUT FILE

with io.open(inputfile, 'r') as f:  
    nb = read(f, as_version=4)
    
# WRITE TO OUTPUT FILE

with open(outputfile, 'w') as myfile:
    for cell in nb.cells:
    
        # Remove one cell 
        if cell['source']=='%pylab inline':
            continue
        
        # Print source code of (remaining) cells to output file
        print >> myfile, cell['source']
        print >> myfile, " \n",  " \n",  " \n"
        
        /Users/burbol2/GitHub/scripts/Python/topfile_creation-cuda.ipynb


