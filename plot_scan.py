# -------------------------------------------------
#
# Script for plotting relaxed surface scans performed
# with orca 4.2.1 using a .dat file
#
# The input format is: 'python plot_scan.py filename.dat'
#
# Output files: filename_plotscan.png
# -------------------------------------------------
# =================================================
# Written by Antonio Garcia Alcaraz 11/2021
# =================================================

import os
import argparse
import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy

if __name__ == "__main__":

    #Create the argument parser
    parser = argparse.ArgumentParser("This script plots energy vs number of steps for a relaxed surface scan done with ORCA using the .dat file")
    parser.add_argument("path", help="The filepath to the file to be analyzed")
    
    args = parser.parse_args()
    filename =args.path
    
    #Read the data from the specified file
    
    file_path = os.path.join(args.path)
    
    file = numpy.genfromtxt(fname=file_path, delimiter=' ', dtype='float')
    
    #Figure out the file name for writing the output
    
    fname = os.path.basename(args.path).split('.')[0]
    
    #Counting number of steps
    
    steps = file[:,0]
    total_steps = len(steps)
    every_step = list(range(1, total_steps+1))
    
    #Plot
    
    plt.figure()
    plt.xlabel('Number of step')
    plt.ylabel('Energy (Eh)')
    plt.plot(every_step, file[:,1], '--o')
    plt.savefig(F'{fname}_plotscan.png')
    
    #Final message
    
    print('Done! {}_plotscan.png has been created.'.format(fname))
    
    
    

    
    
            
   

        
        
    
            

    

    