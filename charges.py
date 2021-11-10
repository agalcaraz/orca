# -------------------------------------------------
#
# Script for printing Mulliken and Loewdin charges from
# a calculation performed in orca 4.2.1 using as input
# a .log file
#
# The input format is: 'python charges.py filename.log'
#
# Output information: Mulliken and Loewdin charges
#
# Output files: filename_charges.txt 
# -------------------------------------------------
# =================================================
# Written by Antonio Garcia Alcaraz 11/2021
# =================================================

import os
import argparse
import matplotlib.pyplot as plt
import sys
import pandas as pd

if __name__ == "__main__":

    #Create the argument parser
    parser = argparse.ArgumentParser("This script parses orca files to extract Mulliken and Loewdin charges")
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
    
    output_location = F'{fname}_charges.txt'
    output = open(output_location, 'w+')
    
    #Checking if the calculation was correctly finished
        
    found = False
    for line in data:
        if 'ORCA TERMINATED NORMALLY' in line:
            found = True
    if not found:
        sys.exit('Calculation not completed. Something went wrong.')

    print('-----------------------------------------')
    print('Charges for {}.log'.format(fname))
    print('-----------------------------------------')
    output.write(f'-----------------------------------------\n')
    output.write(f'Data for {fname}.log\n')
    output.write(f'-----------------------------------------\n')
    
    #Printing charges
    
    mulliken_lines = []
    mulliken_reduced_lines = []
    
    for linenum, line in enumerate(data):
        if 'MULLIKEN ATOMIC CHARGES' in line:
            mulliken_line = linenum
            mulliken_lines.append(mulliken_line)
        if 'MULLIKEN REDUCED ORBITAL CHARGES' in line:
            mulliken_reduced_line = linenum
            mulliken_reduced_lines.append(mulliken_reduced_line)
    
    final_mulliken_line = mulliken_lines[-1]
    final_mulliken_reduced_line = mulliken_reduced_lines[-1]
    
    mulliken_list = data[final_mulliken_line+2:final_mulliken_reduced_line-3]
    
    num_atom_list = ['Nº']
    symbols_list = ['Atom']
    mulliken_charges_list = ['Mulliken']
    mulliken_charges_list_float = []
    
    for line in mulliken_list:
        mulliken_list_split = line.split()
        num_atom_values = mulliken_list_split[0]
        num_atom_list.append(num_atom_values)
        symbols = mulliken_list_split[1]
        symbols_list.append(symbols)
        mulliken_atom_charges = mulliken_list_split[3]
        mulliken_charges_list.append(mulliken_atom_charges)
        mulliken_atom_charges_float = float(mulliken_atom_charges)
        mulliken_charges_list_float.append(mulliken_atom_charges_float)
        
    loewdin_lines = []
    loewdin_reduced_lines = []
    
    for linenum, line in enumerate(data):
        if 'LOEWDIN ATOMIC CHARGES' in line:
            loewdin_line = linenum
            loewdin_lines.append(loewdin_line)
        if 'LOEWDIN REDUCED ORBITAL CHARGES' in line:
            loewdin_reduced_line = linenum
            loewdin_reduced_lines.append(loewdin_reduced_line)
    
    final_loewdin_line = loewdin_lines[-1]
    final_loewdin_reduced_line = loewdin_reduced_lines[-1]
    
    loewdin_list = data[final_loewdin_line+2:final_loewdin_reduced_line-2]
    
    loewdin_charges_list = ['Loewdin']
    loewdin_charges_list_float = []
    
    for line in loewdin_list:
        loewdin_list_split = line.split()
        loewdin_atom_charges = loewdin_list_split[3]
        loewdin_charges_list.append(loewdin_atom_charges)
        loewdin_atom_charges_float = float(loewdin_atom_charges)
        loewdin_charges_list_float.append(loewdin_atom_charges_float)

    net_mulliken_charge = sum(mulliken_charges_list_float)
    net_mulliken_charge_formatted = '{0:.6f}'.format(net_mulliken_charge) #Formatting the number to have 6 decimals
    net_mulliken_charge_str = str(net_mulliken_charge_formatted)
    mulliken_charges_list.append(net_mulliken_charge_str)
    net_loewdin_charge = sum(loewdin_charges_list_float)
    net_loewdin_charge_formatted = '{0:.6f}'.format(net_loewdin_charge)
    net_loewdin_charge_str = str(net_loewdin_charge_formatted)
    loewdin_charges_list.append(net_loewdin_charge_str)
    last = '-'
    num_atom_list.append(last)
    suma = 'Sum'
    symbols_list.append(suma)
    table = '\n'.join('{}\t{}\t{} \t{} '.format(w, x, y, z) for w, x, y, z in zip(num_atom_list, symbols_list, mulliken_charges_list, loewdin_charges_list))
    print(table)
    output.write(table) 
    
    output.close()
        

    
    
            
   

        
        
    
            

    

    