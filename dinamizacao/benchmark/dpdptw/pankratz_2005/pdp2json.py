import pandas as pd
import os



os.listdir
directory = "./DPDPTW-Instances/exante0/"   
filename = "lc101_a010_q0.pdp"
instance_dict = {}


def read_until(filename, flag):
    current_line = filename.readline()
    line_dict = {}
    while(current_line != flag):
        line_info = current_line.split() 
        line_dict[line_info[0]] = line_info[1]
        current_line = filename.readline()
    return line_dict

def get_static_info(from_file):
    flag = "NODE_COORD_SECTION:\n"
    return read_until(from_file, flag)

def get_coordinates_info(from_file, to_dict):
    flag = "NODE_COORD_SECTION:\n"
    current_line = from_file.readline() 
    while(current_line != flag):
        line_info = current_line.split() 
        to_dict[line_info[0]] = line_info[1]
        current_line = from_file.readline()





with open(directory + filename) as instace_file:
    instance_dict = get_static_info(instace_file)
        
    