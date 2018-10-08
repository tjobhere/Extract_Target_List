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

#This function is for reading each row of the specified file and loading them into a list
def load_list(file_name,list_for_loading):
    print('Loading items from  : ',file_name)
    f=open(file_name,'r')
    while True:
        line=f.readline()
        if len(line)==0:
            break
        else:
#            print(line,end='')
            #check if the last character read in the line is a newline char. If so eliminate it while appending to the list
            if line[-1]=='\n':
                list_for_loading.append(line[0:-1])
            else:
                list_for_loading.append(line)
    f.close()
    #print('List in load_list :',list_for_loading)
    return

#This is function will check return the list items in List2 that are not present in List1
# Items not found are added to the List3
def compare(List1,List2,List3):
    for item2 in List2:
#        print('Comparing item : ',item2)
        flag=True
        for item1 in List1:
#            print('Comparing with item : ',item1)
            if item2==item1:
#                print('Match found')
                flag=False
                break
        if flag==True:
#           print('Match not found. Adding..')
            List3.append(item2)
#    print('Done.')
    return

#Write the New_list to the output file
def write_list(file_for_writing,List):
    print('Writing to file :',file_for_writing)
    f=open(file_for_writing,'w')
    for item in List:
        f.write(item+',')
    f.close()

cwd=os.getcwd()
print('Current Working Directory : ',cwd)
#Load the Master file
Lifer_file='Lifer.csv'
Lifer_list=[]
load_list(Lifer_file,Lifer_list)
#print('List in Main : ',Lifer_list)

#Load the File_for_Compare
To_compare_file='Location_list.csv'
Location_list=[]
load_list(To_compare_file,Location_list)
#print('List in Main : ',Location_list)

#Compare
New_list=[]
compare(Lifer_list,Location_list,New_list)
print('New items are : ',New_list)

#Write the New_list into the target file
Potential_Lifers_file='Potential_Lifers.csv'
write_list(Potential_Lifers_file,New_list)
#load_list(Potential_Lifers_file,Lifer_list)
#print('List in Main : ',Lifer_list)