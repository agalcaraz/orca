# -------------------------------------------------
#
# Script for parsing main information of a geometry
# optimization (without vibrational frequencies calculation) 
# done in orca 4.2.1 using as input a .log file
#
# The input format is: 'python geom_opt.py filename.log'
#
# Output information: electronic parameters and 
# energy vs nº cycles representation
#
# Output files: filename.txt & filename.png
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
    parser = argparse.ArgumentParser("This script parses optimization files done in orca to extract final single point energy, molecular orbitals and the energy vs number cycles representation")
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
    
    output_location = F'{fname}.txt'
    output = open(output_location, 'w+')
    
    #Checking if the calculation was correctly finished
    
    found = False
    for line in data:
        if 'OPTIMIZATION RUN DONE' in line:
            found = True
    if not found:
        sys.exit('Optimization not completed, something went wrong.')
        
    found = False
    for line in data:
        if 'ORCA TERMINATED NORMALLY' in line:
            found = True
    if not found:
        sys.exit('Calculation not completed.')

    print('-----------------------------------------')
    print('Data for {}.log'.format(fname))
    print('-----------------------------------------')
    output.write(f'-----------------------------------------\n')
    output.write(f'Data for {fname}.log\n')
    output.write(f'-----------------------------------------\n')
    
    #Printing energy, zpe and g correction
    
    all_energies = []

    for line in data:
        if 'FINAL SINGLE POINT ENERGY' in line:
            energy_line = line
            energy_line_split = energy_line.split()
            energy_values = float(energy_line_split[-1])
            all_energies.append(energy_values)  

    print('Final single point energy (Eh) : {}'.format(all_energies[-1]))
    output.write(f'Final single point energy (Eh) : {all_energies[-1]}\n')
    
    #Printing number of atoms
    
    for linenum, line in enumerate(data):
        if '*xyz' in line:
            xyz_line = linenum
        if '****END OF INPUT****' in line:
            end_line = linenum
    first_atom = xyz_line + 2
    last_atom = end_line - 1
    num_atom = last_atom - first_atom
    
    #Printing molecular orbitals
    
    orbital_lines = []
    mulliken_lines = []
    
    for linenum, line in enumerate(data):
        if 'ORBITAL ENERGIES' in line:
            orbital_line = linenum
            orbital_lines.append(orbital_line)
        if '* MULLIKEN POPULATION ANALYSIS *' in line:
            mulliken_line = linenum
            mulliken_lines.append(mulliken_line)
    
    final_orbital_line = orbital_lines[-1]
    final_mulliken_line = mulliken_lines[-1]
    
    orbital_list = data[final_orbital_line+4:final_mulliken_line-2]
    
    occupancy_list = []
    orbital_energies_list = []
    
    for line in orbital_list:
        orbital_list_split = line.split()
        occupancy_values = float(orbital_list_split[1])
        occupancy_list.append(occupancy_values)
        orbital_energies_values = float(orbital_list_split[3])
        orbital_energies_list.append(orbital_energies_values)
        
    occupied_list = []
    
    for number in occupancy_list:
        if number == 2:
            occupied_list.append(number)
    
    length_occupied_list = len(occupied_list)
    
    HOMO = orbital_energies_list[length_occupied_list-1]
    LUMO = orbital_energies_list[length_occupied_list]
    gap = LUMO - HOMO
    
    print('Energy HOMO (eV) : {} / MO nº: {}'.format(HOMO, length_occupied_list-1))
    print('Energy LUMO (eV) : {} / MO nº: {}'.format(LUMO, length_occupied_list))
    print('gap HOMO-LUMO (eV) : {}'.format(gap))
    output.write(f'Energy HOMO (eV) : {HOMO} / MO nº: {length_occupied_list-1}\n')
    output.write(f'Energy LUMO (eV) : {LUMO} / MO nº: {length_occupied_list}\n')
    output.write(f'gap (eV) : {gap}\n')
    
    #Plotting energies vs number of cycles 
    
    all_cycles = []
    
    for line in data:
        if 'GEOMETRY OPTIMIZATION CYCLE' in line:
            cycle_line = line
            cycle_line_split = cycle_line.split()
            numbers = float(cycle_line_split[-2])
            all_cycles.append(numbers)
    
    plt.figure(figsize = (10,5))
    plt.xlabel('Number of cycles')
    plt.ylabel('Energy (Eh)')
    plt.plot(all_cycles, all_energies[:-1], '--o')
    plt.savefig(F'{fname}.png', bbox_inches = 'tight')
    
    output.close()
    
    
            
   

        
        
    
            

    

    