# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:44:56 2018

@author: tjob
"""
# The objective of this program is to compare the list of items in
# two files (Master and File_for_Compare) and identify the items in File_for_Compare which are not there in Master.
# The identified items are written into a third file called New_Items
# Presently the program is expected to run in Windows, from a directory convention viewpoint

import os
import argparse

#This function eliminates the unwanted tabs, quotes and newline characters in the given string
#It will also eliminate any trailing space in the cleaned string before returning
def clean_string(str):
    length_of_str=len(str)
    #print('Uncleaned String :#',str,'#')
    #print("Length of string is :",length_of_str)
    i=0
    cleaned_str=""
    to_eliminate=['\n','\t','\"']
    while i<length_of_str:
        if str[i] in to_eliminate:
            i+=1
        else:
            cleaned_str=cleaned_str.__add__(str[i])
            i+=1
    #print('Cleaned String :#',cleaned_str,'#, Length:',len(cleaned_str))
    #Check if the last character is a space. If so eliminate it
    if len(cleaned_str)>0 and cleaned_str[-1]==' ':
        return cleaned_str[0:-1]
    else:
        return cleaned_str


#This function is for reading each row of the specified file and loading them into a list
def load_list(file_name,list_for_loading,file_type,verbose):
    print('Loading items from  : ',file_name)
    f=open(file_name,'r')
    while True:
        line=f.readline()
        if len(line)==0:
            break
        else:
            if verbose==True:
                print(line,end='')
            #check if the last character read in the line is a newline char. If so eliminate it while appending to the list
            #Also check if there is an extra blank character at the end. If so eliminate it while appending to the list
            if file_type=="Master":
                if len(line)>1:
                    if line[-1]=='\n':
                        if line[-2]==' ':
                            list_for_loading.append(line[0:-2])
                        else:
                            list_for_loading.append(line[0:-1])
                elif line[0]=='\n':
                     continue
                else:
                    list_for_loading.append(line)
            else:
                cln_str=clean_string(line)
                if len(cln_str)>0:
                    #print('loading string:#',cln_str,'#')
                    list_for_loading.append(cln_str)
    f.close()
    if verbose==True:
        print('The loaded list is :',list_for_loading)
    return

#This is function will check return the list items in List2 that are not present in List1
# Items not found are added to the List3
def compare(List1,List2,List3,verbose):
    for item2 in List2:
        if verbose==True:
            print('Comparing item : ',item2)
        flag=True
        for item1 in List1:
            if verbose==True:
                print('Comparing with item : ',item1)
            if item2==item1:
                if verbose==True:
                    print('Match found')
                flag=False
                break
        if flag==True:
            if verbose==True:
                print('Match not found. Adding..')
            List3.append(item2)
    if verbose==True:
        print('New Items : ',List3)
    return

#Write the New_list to the output file
def write_list(file_for_writing,List):
    print('Writing to file :',file_for_writing)
    f=open(file_for_writing,'w')
    for item in List:
        f.write(item+','+'\n')
    f.close()

#Parse the command line arguments first
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true",help="Increase output verbosity")
parser.add_argument("-d", "--directory", help="Specify the working directory")
parser.add_argument("-m", "--master", help="Specify the name of the MASTER file")
parser.add_argument("-c", "--compare", help="Specify the name of file to compare")
args=parser.parse_args()
if args.verbose:
    verbose=True
else:
    verbose=False
if args.directory!=None:
#    print('Changing to CWD : ',args.directory)
    os.chdir(args.directory)
    print("New Working Directory is :",os.getcwd())
else:
    print('Current Working Directory : ',os.getcwd())

if args.master!=None:
    Lifer_file=args.master
else:
    Lifer_file='Lifer.csv'
print(Lifer_file)

if args.compare!=None:
    To_compare_file=args.compare
else:    
    To_compare_file='Location_list.csv'
print(To_compare_file)


#Load the Master file
Lifer_list=[]
load_list(Lifer_file,Lifer_list,"Master",verbose)
#print('List in Main : ',Lifer_list)

#Load the File_for_Compare
Location_list=[]
load_list(To_compare_file,Location_list,"To_Compare",verbose)
#print('List in Main : ',Location_list)

#Compare
New_list=[]
compare(Lifer_list,Location_list,New_list,verbose)
#print('New items are : ',New_list)

#Write the New_list into the target file
Potential_Lifers_file='Potential_Lifers.csv'
write_list(Potential_Lifers_file,New_list)
#load_list(Potential_Lifers_file,Lifer_list)
#print('List in Main : ',Lifer_list)
