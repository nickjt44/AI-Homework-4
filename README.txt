********** README FOR CSC 520 HOMEWORK 4 QUESTION 2 ***********

This program implements a Truth Maintenance System as specified in the assignment.

The program is all on one file, called TMS.py, and is implemented in Python.

On the second line of the class (TMS) definition, one can change the name of the input file that the program reads.

The program is called at the bottom of the file, where it iterates through the text file, builds and adjusts the knowledge base,
and prints out the state of the knowledge base at the end of the program's run.

The final output consists of the line "State of TMS", followed by everything contained in the knowledge base below it.

The contents of the knowledge base are unordered, so they may be in a different order to what is expected, but hopefully the
correct values should all be there.   The knowledge base is divided into two data structures, a list and a dictionary, which contain
explicitly added literals/statements, and implied literals, respectively.

Other than that, you should just need to run the program.

The code became quite convoluted in places, but I have added comments to describe what the main functions and data structures do.

