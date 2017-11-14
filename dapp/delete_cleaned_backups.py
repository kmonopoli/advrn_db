"""
Created on Thu Jun  2 12:20:36 2016

@author: kathryn_monopoli
"""

import os.path
from database_backup_cleaner import DBBackup_Cleaner

Cleaner = DBBackup_Cleaner()

fileList = os.listdir(Cleaner.trash)
mysql_file_list = []


for f in fileList:
    # removes any files that are not mysql files from the list of files to delete
    if f.__contains__("mysql"):
        mysql_file_list.append(f)

print "Deleting ",len(mysql_file_list)," files"
        
for f in mysql_file_list:
    # deletes all files in the list
    os.remove(Cleaner.trash+"/"+f)

    
