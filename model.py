# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 08:40:56 2020

@author: DaMol
"""

import os
import pathlib
import pandas as pd
import datetime
import argparse
import sys

# parser = argparse.ArgumentParser(description='Converts an FDS output to an Excel file.')
# parser.add_argument('input', metavar='input', type=str, nargs='+',
#                     help='input file as standard text file')
# parser.add_argument('output', metavar='ouput', type=str, nargs='+',
#                     help='output excel file name')


# args = parser.parse_args()
# print(args)

# import pyinstaller

default_input = "output.out"

def FDS2Excel(input_file=default_input, output_name="output.xlsx"):

	with open(input_file, 'r') as f:
		lines = f.readlines()
	   
	full_list=[]
	RTD = 0
	i=0
	end_words="DEVICE Activation Times"

	tag1="Time Step"
	tag2="Step Size"
	tag3="Pressure Iterations"
	tag4="Maximum Velocity Error"
	tag5="Maximum Pressure Error"

	for l in lines:
		i+=1
		# print(i)
		if "Run Time Diagnostics" in l:
			RTD = 1
			continue
		if RTD == 0:
			continue
		
		# RT0 = 1 in this section
		if any(w in l for w in [tag1, tag2, tag3, tag4, tag5]):
			# print(l)
			pass
		
		if tag1 in l:
			time_step = l[17:24]
			full_date = l[24:].strip()
			
		if tag2 in l:
			step_size = float(l[17:30])
			total_time = float(l[45:56].strip())
			
		if tag3 in l:
			pressure_iter = float(l[27:].strip())
			
		if tag4 in l:
			mve_value = float(l[30:40].strip())
			mve_mesh = int(l[48:52].strip())
			mve_cell = l[57:69].strip()
			
		if tag5 in l:
			mpe_value = float(l[30:40].strip())
			mpe_mesh = int(l[48:52].strip())
			mpe_cell = l[57:69].strip()
			# print(time_step, full_date, step_size, total_time, pressure_iter, \
			#       mve_value, mve_mesh, mve_cell, mpe_value, mpe_mesh, mpe_cell,)
			comput_time=0 #placeholder
			comput_time_days=0
			full_list.append([time_step, full_date, comput_time, comput_time_days, step_size, total_time, pressure_iter, \
				  mve_value, mve_mesh, mve_cell, mpe_value, mpe_mesh, mpe_cell])
			
		
		
		
		
		
		if end_words in l:
			break
		# print(l)
	
	  
	

	if full_list != []:
		df=pd.DataFrame(full_list)
		df.iloc[:,2]=df.iloc[:,1]
		df.iloc[:,2]=df.iloc[:,2].apply(lambda x: \
										(datetime.datetime.strptime(x, '%B %d, %Y %H:%M:%S') - \
											datetime.datetime.strptime(df.iloc[0,1], \
																	'%B %d, %Y %H:%M:%S')).total_seconds())
		df.iloc[:,3]=df.iloc[:,2]/86400
	

			
		# March 16, 2020  17:41:50
		# d1= datetime.datetime.strptime(df.iloc[0,1], '%B %d, %Y %H:%M:%S')
		# d2= datetime.datetime.strptime(df.iloc[1,1], '%B %d, %Y %H:%M:%S')
		# d3=d2-d1
		# print(int(d3.total_seconds()))

		
		df.to_excel(output_name, \
										header=["Time step", "Date", "Computational time (s)", "Computational time (days)", "Step size (s)", "Simulation time (s)", \
												"Pressure iterations", "Maximum Velocity Error", "At Mesh", "At Cell",\
													"Maximum Pressure Error", "At Mesh", "At Cell"]
		, \
											index=False)


	else:
		pd.DataFrame(["The input full that was uploaded is not supported"]+[0]*12).to_excel(output_name, \
									 header=["Time step", "Date", "Computational time (s)", "Computational time (days)", "Step size (s)", "Simulation time (s)", \
											 "Pressure iterations", "Maximum Velocity Error", "At Mesh", "At Cell",\
												 "Maximum Pressure Error", "At Mesh", "At Cell"]
	, \
										 index=False)


	print('Parsing successful.')

if __name__ == "__main__":
    print((sys.argv[1], sys.argv[2]))
    FDS2Excel(sys.argv[1], sys.argv[2])
