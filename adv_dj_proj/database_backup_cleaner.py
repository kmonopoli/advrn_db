# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:25:56 2016

Database Backup Cleanup
Keeps in permanant storage:
- At 12:00 1st and 15th of every month

Keeps in temporary storage:
- Past 24 hours
- At 9:00, 12:00, 17:00 in past 7 days
- At 12:00 in past 30 days


@author: kathryn_monopoli
"""
import os.path, time
from settings import DBBACKUP_BACKUP_DIRECTORY
import shutil
import glob



class DBBackup_Cleaner:
    
    dbbackup_dir = "" ## Path to directory where Django_Database_Backup app stores backups
    file_list = [] ## List of DB_File Objects corresponding to files in dbbackup_dir
    cur_time = time.localtime(time.time())
    cur_time_sec = time.time()
    

    perm_backup_dir =  DBBACKUP_BACKUP_DIRECTORY+"/permanent_backups" ## Directory where permantent backups go
    trash = DBBACKUP_BACKUP_DIRECTORY+"/to_be_deleted" # Files that will be deleted are placed in this directory temporarily
    
    def __init__(self):
        self.dbbackup_dir = DBBACKUP_BACKUP_DIRECTORY ## from settings.py
        self.make_dirs()
        self.get_files(self.dbbackup_dir)


    def get_files(self, directory):
        ## Returns a list of DB_File objects for files within directory
        db_file_list = []
        fileList = os.listdir(directory)
        for fname in fileList:
            if fname.__contains__(".mysql"):
                db_file_list.append(DB_File(fname,self.dbbackup_dir))
        self.file_list = db_file_list
        return
        
        """
        Get all database files from DBBACKUP_BACKUP_DIRECTORY
        - move any files from 12:00 1st and 15th of month to permanent storage
        - move any files with "manual_backup" in the name to permanent storage  
        Keeps in temporary storage:
        - Past 24 hours
        - At 9:00, 12:00, 17:00 in past 7 days
        - At 12:00 in past 30 days
        Rest go to trash - will be deleted with delete_cleaned_backups.py
        """
    def make_dirs(self):
        # makes permanent_backups and to_be_deleted directories if they do not exist in the DBBACKUP_BACKUP_DIRECTORY
        dirLs = os.listdir(DBBACKUP_BACKUP_DIRECTORY)
        if not dirLs.__contains__("permanent_backups"):
            os.mkdir(self.perm_backup_dir)
        if not dirLs.__contains__("to_be_deleted"):
            os.mkdir(self.trash)
      
    
    def process_files(self):
        self.get_manual_backups()
        self.get_longterm_backups()
        self.get_longterm_backups_2()
        self.get_past_day()
        self.get_past_week()
        self.get_past_month()
        print "Number of files to delete: ",len(self.file_list)
        self.cleanup()
        return

    def get_manual_backups(self):
        ## Finds files labelled as "manual_backup" and moves to longterm
        ls = []
        for f in self.file_list:
            if f.name.__contains__("manual_backup"):
                ls.append(f)
        self.file_list = [item for item in self.file_list if item not in ls] 
        self.move_to(ls,self.perm_backup_dir)
        return
    
    def get_longterm_backups(self):
        ## Finds files from 12:00 1st and 15th of every month and moves to permanent backups
        ls =[]
        for f in self.file_list:
            if (f.day == 15) or (f.day == 1):
                if (f.hour == 12):
                    ls.append(f)
        print "Number of files to keep longterm: ", len(ls)
        self.file_list = [item for item in self.file_list if item not in ls]
        self.move_to(ls,self.perm_backup_dir)
        return
    def get_longterm_backups_2(self):
        ## If no files in permanent backups directory are from from past 2 weeks, moves the most recent backup to permanent backups
        print "Getting long term backups"
        newest = max(glob.iglob('*.mysql'), key = os.path.getctime) # gets newest mysql file
        direct = os.getcwd()
        os.chdir(self.perm_backup_dir)
        newest_perm = max(glob.iglob('*.mysql'), key = os.path.getctime) # gets newest mysql file in perm_backup_dir
        t_newest = os.path.getctime(newest_perm)
        self.get_days((time.time() - t_newest))
        if (time.time() - t_newest) > (604800*2): # seconds in 2 weeks
            ## if there are no backups within past 2 weeks need to move most recent file to perm_backup_dir
            shutil.move(direct+"/"+newest, self.perm_backup_dir) # move file
            print newest, " moved to permanent backups"
        else:
            print "No files to move to permanent backups!"
        os.chdir(direct)
        return
        

    def get_past_day(self):
        ## Finds files from past 24 hours and removes from file_list
        ls =[]
        for f in self.file_list:
            x = self.cur_time_sec - f.crt_time_sec
            if x <= 86400: # seconds in a day
                ls.append(f)
        self.file_list = [item for item in self.file_list if item not in ls] 
        return
    
    def get_days(self,n):
        mins = n/60
        hrs = mins/60
        days = hrs/24
        print days, " days"
    
    def get_past_week(self):
        ## Finds files from past week created at 9:00,12:00,17:00 and removes from file_list
        ls = []
        for f in self.file_list:
            x = self.cur_time_sec - f.crt_time_sec
            if x <= 604800: # seconds in a week
                if (f.hour == 9) or (f.hour == 12) or (f.hour == 17):
                    ls.append(f)
        self.file_list = [item for item in self.file_list if item not in ls] 
        return
        
    def get_past_month(self):
        ## Finds files from past month created at 12:00 and removes from file_list
        ls = []
        for f in self.file_list:
            x = self.cur_time_sec - f.crt_time_sec
            if x <= 2592000: # seconds in a month
                if (f.hour == 12):
                    ls.append(f)
        self.file_list = [item for item in self.file_list if item not in ls] 
        return  
        
    def cleanup(self):
        ## Moves any remaining files in file_list to trash
        for f in self.file_list:
            shutil.move(f.path, self.trash)
        for f in self.file_list:
            self.file_list.remove(f)

    def move_to(self,ls,directory):
        ## Moves file list to indicated directory 
        for f in ls:
            shutil.move(f.path, directory)
        return
        
        

class DB_File:
    name = ""
    path = ""
    ## Date Created:
    day = 0
    month = 0
    year = 0
    hour = 0
    crt_time_sec = 0 ## 
    
    def __init__(self,name,path):
        os.chdir(path)
        self.name = name
        self.path = path + "/" + self.name
        self.set_datetime_created()
        

    
    
    def set_datetime_created(self):
        self.crt_time_sec = os.path.getctime(self.name)
        dt = time.struct_time(time.localtime(self.crt_time_sec))
        self.day = dt.tm_mday
        self.month = dt.tm_mon
        self.year = dt.tm_year
        self.hour = dt.tm_hour
        
        return
        
        
        

"""
RUN MODULE
"""

x = DBBackup_Cleaner()
print "Number of files to process ", len(x.file_list)
x.process_files()
