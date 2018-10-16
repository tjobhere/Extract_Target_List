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
import sys

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

#This function will eliminate loading the alternate english name for a species as sometimes seen in the Lifer file
#This will help eliminate of false positives owing to such cases since the hotspot list does not contain them
def eliminate_alternate_name(name):
    i=0
    cleaned_name=""
    while i<len(name) and name[i]!='(':
        cleaned_name=cleaned_name.__add__(name[i])
        i+=1
    if cleaned_name[-1]==' ':
        return cleaned_name[0:-1]
    else:
        return cleaned_name

#This function is for reading each row of the specified file and loading them into a list
#It loads taking into account the specific aspects of the files
def load_list_master(file_name,list_for_loading,verbose):
    print('Loading items from :',file_name)
    f=open(file_name,'r')
    #Reads the first line and understand which column will hold the Species name. It assumes that the first row in the file is the Header
    line=f.readline()    
    if len(line)<8:
        print('ERROR : No valid HEADER found in the Lifer file! Exiting!')
        f.close()
        sys.exit(1)
    species_column=1
    i=0
    hdr_str=""
    found_tag=0
    while True:
        if line[i]!=',' and line[i]!='\n':
            hdr_str=hdr_str.__add__(line[i])
        #print('Current Str :!',hdr_str,'!')
        if line[i]==',' or line[i]=='\n':
            if hdr_str.upper()=='SPECIES':
                found_tag=1
                break
            species_column+=1
            hdr_str=""
            i+=1
        else:
            i+=1
      
    if found_tag==0:
        print('ERROR : SPECIES column not found in HEADER of the Lifer file! Exiting!')
        f.close()
        sys.exit(1)
    print('Found Species in position ',species_column,' of Header')
    row=2
    while True:
        line=f.readline()
        if len(line)==0:
            break
        else:
            if verbose==True:
                print(line,end='')
            #First find the Species name based on species_column value set earlier
            if len(line)>1:
                column_cntr=1
                i=0
                data_str=""
                found_tag=0
                while True:
                    if line[i]!=',' and line[i]!='\n':
                        data_str=data_str.__add__(line[i])
                    if line[i]==',':
                        if column_cntr==species_column:
                            if len(data_str)>0:
                                found_tag=1
                                row+=1
                                break
                            else:
                                print('Data Error in row :',row,'. Skipping row.')
                                row+=1
                                break
                        else:
                            data_str=""
                            column_cntr+=1
                            i+=1
                    elif line[i]=='\n':
                        if column_cntr==species_column:
                            found_tag=1
                            row+=1
                            break
                        else:
                            print('Data Error in row :',row,'. Skipping row.')
                            row+=1
                            break
                    else:
                        i+=1
                if found_tag==1:
                    if '(' in data_str:
                        data_str=eliminate_alternate_name(data_str)
                    list_for_loading.append(data_str)
            
    f.close()
    if verbose==True:
        print('The loaded Master list is :',list_for_loading)
    return

#This function is for reading each row of the specified file and loading them into a list
#It loads taking into account the specific aspects of the files
def load_list_hotspot(file_name,list_for_loading,verbose):
    print('Loading items from  : ',file_name)
    f=open(file_name,'r')
    while True:
        line=f.readline()
        if len(line)==0:
            break
        else:
            if verbose==True:
                print(line,end='')
            #If it is a generic species entry, (represented by sp.) or two similar species (represented by /) then exclude
            if "sp." in line:
                continue
            elif "/" in line:
                continue
            cln_str=clean_string(line)
            if len(cln_str)>0:
                #print('loading string:#',cln_str,'#')
                list_for_loading.append(cln_str)
    f.close()
    if verbose==True:
        print('The loaded Hotspot list is :',list_for_loading)
    return

#This is function will check return the list items in List2 that are not present in List1
# Items not found are added to the List3
#The comparison is case insensitive
def compare(List1,List2,List3,verbose):
    for item2 in List2:
        if verbose==True:
            print('Comparing item : ',item2)
        flag=True
        for item1 in List1:
            if verbose==True:
                print('Comparing with item : ',item1)
            if item2.upper()==item1.upper():
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
parser.add_argument("-d", "--directory", help="Specify the working directory, The inputs files and the output file will be in this directory")
parser.add_argument("-m", "--master", help="Specify the name of the MASTER file")
parser.add_argument("-c", "--compare", help="Specify the name of file to compare")
parser.add_argument("-o", "--output", help="Specify the name of the output file")
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
    To_compare_file='ebird_scraped.csv'
print(To_compare_file)

if args.output!=None:
    Potential_Lifers_file=args.output
else:
    Potential_Lifers_file='Potential_Lifers.csv'

#Load the Master file
Lifer_list=[]
load_list_master(Lifer_file,Lifer_list,verbose)
#print('List in Main : ',Lifer_list)

#Load the File_for_Compare
Location_list=[]
load_list_hotspot(To_compare_file,Location_list,verbose)
#print('List in Main : ',Location_list)

#Compare
New_list=[]
compare(Lifer_list,Location_list,New_list,verbose)
#print('New items are : ',New_list)

#Write the New_list into the target file
write_list(Potential_Lifers_file,New_list)
#load_list(Potential_Lifers_file,Lifer_list)
#print('List in Main : ',Lifer_list)
