# -------------------------------------------------
#
# Script for printing final energy value of single 
# point calculation performed with orca 4.2.1 using 
# as input a .log file
#
# The input format is: 'python final_energy filename.log'
#
# Output information: final single point energy
#
# Output files: filename_finalenergy.txt 
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
    parser = argparse.ArgumentParser("This script prints the final energy value of single point calculation performed with orca 4.2.1")
    parser.add_argument("path", help="The filepath to the file to be analyzed")
    
    args = parser.parse_args()
    filename =args.path
    
    #Read the data from the specified file
    outfile = open(filename)
    data = outfile.readlines()
    outfile.close()
    
    #Figure out the file name for writing the output
    fname = os.path.basename(args.path).split('.')[0]
    
    # Open a file for writing
    
    output_location = F'{fname}_finalenergy.txt'
    output = open(output_location, 'w+')
    
    #Checking if the calculation was correctly finished
        
    found = False
    for line in data:
        if 'ORCA TERMINATED NORMALLY' in line:
            found = True
    if not found:
        sys.exit('Calculation not completed. Something went wrong.')

    print('-----------------------------------------')
    print('Data for {}.log'.format(fname))
    print('-----------------------------------------')
    output.write(f'-----------------------------------------\n')
    output.write(f'Data for {fname}.log\n')
    output.write(f'-----------------------------------------\n')
    
    #Printing final single point energy
    
    all_energies = []

    for line in data:
        if 'FINAL SINGLE POINT ENERGY' in line:
            energy_line = line
            energy_line_split = energy_line.split()
            energy_values = float(energy_line_split[-1])
            all_energies.append(energy_values)  

    print('Final single point energy (Eh) : {}'.format(all_energies[-1]))
    output.write(f'Final single point energy (Eh) : {all_energies[-1]}\n')
    
    output.close()
    
    
            
   

        
        
    
            

    

    