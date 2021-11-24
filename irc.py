# -------------------------------------------------
#
# Script for plotting energy vs step in an irc calc.
# done in orca 4.2.1 using as input a .log file
#
# The input format is: 'python irc.py filename.log'
#
# Output information: energy vs step plot
#
# Output files: filename_plotirc.png
# -------------------------------------------------
# =================================================
# Written by Antonio Garcia Alcaraz 11/2021
# =================================================

import os
import argparse
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":

    #Create the argument parser
    parser = argparse.ArgumentParser("This script parses optimization files done in orca to extract final single point energy, zero point energy, g correction, molecular orbitals and the energy vs number cycles representation")
    parser.add_argument("path", help="The filepath to the file to be analyzed")
    
    args = parser.parse_args()
    filename =args.path
    
    #Read the data from the specified file
    outfile = open(filename)
    data = outfile.readlines()
    outfile.close()
    
    #Figure out the file name for writing the output
    fname = os.path.basename(args.path).split('.')[0]
    
    
    #Checking if the calculation was correctly finished
        
    found = False
    for line in data:
        if 'ORCA TERMINATED NORMALLY' in line:
            found = True
    if not found:
        sys.exit('Calculation not completed.')
    
    #Reading IRC path summary
    
    for linenum, line in enumerate(data):
        if 'IRC PATH SUMMARY' in line:
            irc_line = linenum
        if 'Timings for individual modules' in line:
            timing_line = linenum
            
    irc_data = data[irc_line+5:timing_line-1]
    
    step_values = []
    energy_values = []
    
    for line in irc_data:
        irc_data_split = line.split()
        step = float(irc_data_split[0])
        step_values.append(step)
        energy = float(irc_data_split[1])
        energy_values.append(energy)
        if 'TS' in line:
            ts_line = line
            ts_line_split = ts_line.split()
            step_ts = ts_line_split[0]
    
    #Plotting step vs energy
    
    plt.figure(figsize = (10,5))
    plt.xlabel('Step')
    plt.ylabel('Energy (Eh)')
    plt.plot(step_values, energy_values, '--o')
    plt.savefig(F'{fname}_plotirc.png', bbox_inches = 'tight')
    
    
    #Final message
    
    print('Done! {}_plotirc.png has been created.'.format(fname))
    print('TS was found at step nº {}'.format(step_ts))
    
    
    
    
    
   
    
    
    
            
   

        
        
    
            

    

    