#p-Median Facility Location Problem
#This script creates a linear programming file to be read into an optimizer.
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Developed by:  James D. Gaboardi, MSGIS
#                03/2015
#                © James Gaboardi


# **Attention** **Adjust the following**
#	74 --> 'c##' needs to changed depending on data and constraint number based on .lp file
#	91 --> 'c##' needs to changed depending on data and constraint number based on .lp file
#	91 --> '= ##\n' needs to changed for the number of facilities to be sited

#   Terminology & General Background for Facility Location and Summation Notation:

#   *        The objective of the p-median Facility Location Problem is to minimize the average cost 
#            of travel (between service facilities and clients).

#   *   [i] - a specific origin
#   *   [j] - a specifc destination
#   *   [n] - the set of origins
#   *   [m] - the set of destinations
#   *   [Ai] - weight at each node (usually population)
#   *   [Cij] - travel costs between nodes
#   *   [Sij] - weighted travel costs [(Ai)(Cij)]
#   *   [Z] - the sum of the weighted travel costs between all origins and destinations multiplied by the decision variables 
#   *   [x#_#] - the decision variable in # row, # column position in the matrix
#   *	[y#] - service facility in the # row
#   *   [p] - the number of facilities to be sited


#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Objective Function 
# The objective of this function is to minimize the average travel cost along the network.
# *** Minimize(Z)
def get_objective_function_p_median(Sij):
    outtext = ' obj: '
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += str(Sij[i,j]) + ' x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp + ' \n'
    outtext = outtext[:-4] + ' \n'
    return outtext

# Assignment Constraints
# This indicates a client can only be served by one facility.
# Each column in the matrix must equal 1.
def get_assignment_constraints(rows):
    counter = 0
    outtext = ''
    for i in range(1,cols+1):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(1,rows+1):
            temp += 'x' + str(j) + '_' + str(i) + ' + '
        outtext += temp[:-2] + '= 1\n'
    return outtext

# Opening Constraints
def get_opening_constraints_p_median(Sij):
    counter = 4
    outtext = ''
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            counter = counter + 1 
            outtext += ' c' + str(counter) + ':  - x' + str(i) + '_' + str(j) + ' + ' + 'y' + str(i) +  ' >= 0\n'
    return outtext

# Facility Constraint
# Indicate how many facilties will be sited in 'outtext' below.
# *** '= 1\n' indicates 1 facility
def get_p_facilities(rows):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        temp += 'y' + str(i)
        outtext += temp + ' + '
	outtext = ' c17:  ' + outtext[:-2] + '= 1\n'
    return outtext

# Declaration of Bounds
def get_bounds_allocation(Sij):
    outtext = ''
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += ' 0 <= x' + str(i+1) + '_' + str(j+1) + ' <= 1\n'
        outtext += temp    
    return outtext

def get_bounds_facility(Sij):
    outtext = ''
    for i in range(rows):
        outtext += ' 0 <= y' + str(i+1) + ' <= 1\n'
    return outtext

# Declaration of Decision Variables (form can be: Binary, Integer, etc.)
# In this case decision variables are binary.
def get_allocation_decision_variables_p_median(Sij):
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += ' x' + str(i) + '_' + str(j) + ' '
        outtext += temp
    return outtext
    
def get_facility_decision_variables_p_median(rows):  
    outtext = ''
    for i in range (1, rows+1):
        outtext += ' y' + str(i) + ' '
    return outtext
 
    
#    3. DATA READS & VARIABLE DECLARATION
'''
########## Weights Matrix
########## Sij -->  [0,     13000,  8000, 15000,
##########           15600,     0, 14400, 13200,
##########           8800,  13200,     0, 11000,
##########           18750, 13750, 12500,     0]
########## Read Sij in as a vector text file.
'''
Ai = np.fromfile('path/Ai.txt', dtype=int, sep='\n')
Ai = Ai.reshape(#, #)
Cij = np.fromfile('path/Cij.txt', dtype=float, sep='\n')
Cij = Cij.reshape(#, #)
Sij = Ai * Cij

# Cost Coefficients for Allocation Decision Variables
Sij = np.fromfile('path/Sij.txt', dtype=int, sep='\n')
# Sij matrix dimensions
Sij = Sij.reshape(4,4)
rows, cols = Sij.shape


#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "p-Median Facility Location Problem\n"
text += "'''\n"
text += 'Minimize\n'          
text += get_objective_function_p_median(Sij)
# Declaration of Constraints
text += 'Subject To\n'                    
text += get_assignment_constraints(rows)
text += get_opening_constraints_p_median(Sij)
text += get_p_facilities(rows)
# Declaration of Bounds
text += 'Bounds\n' 
text += get_bounds_allocation(Sij)
text += get_bounds_facility(Sij)
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
text += get_allocation_decision_variables_p_median(Sij)
text += get_facility_decision_variables_p_median(rows)
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"                


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('path/name.lp', 'w')
outfile.write(text)
outfile.close()